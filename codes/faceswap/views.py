import os
from django.shortcuts import render
from .models import FaceSwap,UploadImage
# Create your views here.
# from .serializers import FaceSwapSerializer
import cv2
import numpy as np
import dlib
import time
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from web import settings
from io import StringIO
import io
import imutils
from .face_keypoints import send_face
from django.http import HttpResponse
import boto3
import uuid
import mimetypes
import urllib.request
# from .utils import realtime_face_swapping_webcam




def extract_index_nparray(nparray):
    index = None
    for num in nparray[0]:
        index = num
        break
    return index


def face_swap_on_a_video(request):
    if request.method == "POST":
        if request.GET.get('search'):
            imgid = request.GET.get('search')
            print("🚀 ~ file: views.py ~ line 27 ~ imgid", imgid)
            obj = UploadImage.objects.get(id=imgid)
            imgget = obj.upload_image
            print("🚀 ~ file: views.py ~ line 27 ~ imgid", imgget)
        elif request.FILES["image"]:
            imgget = request.FILES["image"]
        vd = request.FILES["video"]
        fm = FaceSwap(image=imgget,video=vd)
        fm.save()


        uploaded_img = request.FILES.get('image')
        upload_video = request.FILES["video"]
        uploaded_img = str(uploaded_img)
        upload_video = str(upload_video)
        
        # Get unique filename using UUID
        # file_name = uploaded_file.name
        file_name_uuid = uuid_file_path(uploaded_img)
        s3_key = 'image/upload/{0}'.format(file_name_uuid)

        content_type, file_url = upload_to_s3(s3_key, uploaded_img)
        print(f"Saving image to s3. member: {file_url}")

        video_name_uuid = uuid_file_path(upload_video)
        s3_key = 'video/upload/{0}'.format(video_name_uuid)
        content_type, video_url = upload_to_s3(s3_key, upload_video)
        print(f"Saving video to s3. member: {video_url}")


       

        url_response = urllib.request.urlopen(file_url)
        img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
        img = cv2.imdecode(img_array, -1)
        vdo = video_url

        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        mask = np.zeros_like(img_gray)

        cap = cv2.VideoCapture(vdo)
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
        indexes_triangles = []

        # Face 1
        faces = detector(img_gray)
        for face in faces:
            landmarks = predictor(img_gray, face)
            landmarks_points = []
            for n in range(0, 68):
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                landmarks_points.append((x, y))

                # cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

            points = np.array(landmarks_points, np.int32)
            convexhull = cv2.convexHull(points)
            # cv2.polylines(img, [convexhull], True, (255, 0, 0), 3)
            cv2.fillConvexPoly(mask, convexhull, 255)

            face_image_1 = cv2.bitwise_and(img, img, mask=mask)

            # Delaunay triangulation
            rect = cv2.boundingRect(convexhull)
            subdiv = cv2.Subdiv2D(rect)
            subdiv.insert(landmarks_points)
            triangles = subdiv.getTriangleList()
            triangles = np.array(triangles, dtype=np.int32)

            indexes_triangles = []
            for t in triangles:
                pt1 = (t[0], t[1])
                pt2 = (t[2], t[3])
                pt3 = (t[4], t[5])

                index_pt1 = np.where((points == pt1).all(axis=1))
                index_pt1 = extract_index_nparray(index_pt1)

                index_pt2 = np.where((points == pt2).all(axis=1))
                index_pt2 = extract_index_nparray(index_pt2)

                index_pt3 = np.where((points == pt3).all(axis=1))
                index_pt3 = extract_index_nparray(index_pt3)

                if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
                    triangle = [index_pt1, index_pt2, index_pt3]
                    indexes_triangles.append(triangle)

        frames_array = []
        while True:
            try:
                _, img2 = cap.read()
                img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
                img2_new_face = np.zeros_like(img2)
                # Face 2
                faces2 = detector(img2_gray)
                for face in faces2:
                    landmarks = predictor(img2_gray, face)
                    landmarks_points2 = []
                    for n in range(0, 68):
                        x = landmarks.part(n).x
                        y = landmarks.part(n).y
                        landmarks_points2.append((x, y))
                    # cv2.circle(img2, (x, y), 3, (0, 255, 0), -1)
                    points2 = np.array(landmarks_points2, np.int32)
                    convexhull2 = cv2.convexHull(points2)
                lines_space_mask = np.zeros_like(img_gray)
                lines_space_new_face = np.zeros_like(img2)

                # Triangulation of both faces
                for triangle_index in indexes_triangles:
                    # Triangulation of the first face
                    tr1_pt1 = landmarks_points[triangle_index[0]]
                    tr1_pt2 = landmarks_points[triangle_index[1]]
                    tr1_pt3 = landmarks_points[triangle_index[2]]
                    triangle1 = np.array([tr1_pt1, tr1_pt2, tr1_pt3], np.int32)

                    rect1 = cv2.boundingRect(triangle1)
                    (x, y, w, h) = rect1
                    cropped_triangle = img[y: y + h, x: x + w]
                    cropped_tr1_mask = np.zeros((h, w), np.uint8)

                    points = np.array([[tr1_pt1[0] - x, tr1_pt1[1] - y],
                                    [tr1_pt2[0] - x, tr1_pt2[1] - y],
                                    [tr1_pt3[0] - x, tr1_pt3[1] - y]], np.int32)

                    cv2.fillConvexPoly(cropped_tr1_mask, points, 255)

                    # Triangulation of second face
                    tr2_pt1 = landmarks_points2[triangle_index[0]]
                    tr2_pt2 = landmarks_points2[triangle_index[1]]
                    tr2_pt3 = landmarks_points2[triangle_index[2]]
                    triangle2 = np.array([tr2_pt1, tr2_pt2, tr2_pt3], np.int32)

                    rect2 = cv2.boundingRect(triangle2)
                    (x, y, w, h) = rect2

                    cropped_tr2_mask = np.zeros((h, w), np.uint8)

                    points2 = np.array([[tr2_pt1[0] - x, tr2_pt1[1] - y],
                                        [tr2_pt2[0] - x, tr2_pt2[1] - y],
                                        [tr2_pt3[0] - x, tr2_pt3[1] - y]], np.int32)

                    cv2.fillConvexPoly(cropped_tr2_mask, points2, 255)

                    # Warp triangles
                    points = np.float32(points)
                    points2 = np.float32(points2)
                    M = cv2.getAffineTransform(points, points2)
                    warped_triangle = cv2.warpAffine(cropped_triangle, M, (w, h))
                    warped_triangle = cv2.bitwise_and(
                        warped_triangle, warped_triangle, mask=cropped_tr2_mask)

                    # Reconstructing destination face
                    img2_new_face_rect_area = img2_new_face[y: y + h, x: x + w]
                    img2_new_face_rect_area_gray = cv2.cvtColor(
                        img2_new_face_rect_area, cv2.COLOR_BGR2GRAY)
                    _, mask_triangles_designed = cv2.threshold(
                        img2_new_face_rect_area_gray, 1, 255, cv2.THRESH_BINARY_INV)
                    warped_triangle = cv2.bitwise_and(
                        warped_triangle, warped_triangle,
                        mask=mask_triangles_designed)
                    img2_new_face_rect_area = cv2.add(img2_new_face_rect_area,
                                                    warped_triangle)
                    img2_new_face[y: y + h, x: x + w] = img2_new_face_rect_area

                # Face swapped (putting 1st face into 2nd face)
                img2_face_mask = np.zeros_like(img2_gray)
                img2_head_mask = cv2.fillConvexPoly(img2_face_mask, convexhull2, 255)
                img2_face_mask = cv2.bitwise_not(img2_head_mask)

                img2_head_noface = cv2.bitwise_and(img2, img2, mask=img2_face_mask)
                result = cv2.add(img2_head_noface, img2_new_face)

                (x, y, w, h) = cv2.boundingRect(convexhull2)
                center_face2 = (int((x + x + w) / 2), int((y + y + h) / 2))

                seamlessclone = cv2.seamlessClone(result, img2, img2_head_mask,
                                                center_face2, cv2.MIXED_CLONE)
                cv2.imshow("img2", img2)
                cv2.imshow("clone", seamlessclone)
                cv2.imshow("result", result)
                frames_array.append(seamlessclone)
                key = cv2.waitKey(1)
                if key == 27:
                    break
            except:
                break
        cap.release()
        cv2.destroyAllWindows()

        path = 'python-base/codes/faceswap/media'
        video = create_video(path, "result1", frames_array,
                        frames_array[0].shape[1], frames_array[0].shape[0], 30)



        video_name_uuid = uuid_file_path(video)
        s3_key = 'video/upload/{0}'.format(video_name_uuid)
        content_type, result_video_url = upload_to_s3(s3_key, video)
        print(f"Saving Result-video to s3. member: {result_video_url}")


        fm1 = FaceSwap(image=file_url, video=vdo)
        fm1.result = result_video_url
        print("fm.result",fm1.result)
        fm1.save()
        
        return render(request, "face_swap_on_a_video.html",{"video":fm1})
    else:
        images= UploadImage.objects.all()
        return render(request, "face_swap_on_a_video.html",{"images":images})



def uuid_file_path(filename):
    if filename:
        ext = filename.split('.')[-1]
    else:
        ext = "png"

    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(filename)

def upload_to_s3(s3_key, uploaded_file):
    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
    key = getattr(settings, 'AWS_ACCESS_KEY_ID', None)
    secret = getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)

    if not key or not secret:
        print("No key or secret found")
        s3_client = boto3.client('s3')
    else:
        print("Use host. key or secret found")
        s3_client = boto3.client(
            's3', aws_access_key_id=key, aws_secret_access_key=secret)

    content_type, _ = mimetypes.guess_type(s3_key)
    s3_client.upload_file(uploaded_file, bucket_name, s3_key,
                             ExtraArgs={'ACL': 'public-read', 'ContentType': content_type})

    return content_type, f'https://s3.amazonaws.com/{bucket_name}/{s3_key}'


def create_video(out_dir, video_id, frame_set, frame_w, frame_h, fps=20):
    video_path = os.path.join(out_dir, str(video_id) + '.mp4')
    outWriter = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'),
                                fps, (frame_w, frame_h), True)
    print("🚀 ~ file: views.py ~ line 215 ~ outWriter", type(outWriter))

    print('Saving video...')
    for i in range(len(frame_set)):
        outWriter.write(frame_set[i])
    outWriter.release()
    return video_path

def realtime_face_swapping_webcam(request):
    img = cv2.imread("barack-obama-12782369-1-402.jpg")
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = np.zeros_like(img_gray)
    cap = cv2.VideoCapture('-1')
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    print("🚀 ~ file: views.py ~ line 233 ~ cap", cap)

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

    indexes_triangles = []

    # Face 1
    faces = detector(img_gray)
    for face in faces:
        landmarks = predictor(img_gray, face)
        landmarks_points = []
        for n in range(0, 68):
            x = landmarks.part(n).x
            y = landmarks.part(n).y
            landmarks_points.append((x, y))

            # cv2.circle(img, (x, y), 3, (0, 0, 255), -1)

        points = np.array(landmarks_points, np.int32)
        convexhull = cv2.convexHull(points)
        # cv2.polylines(img, [convexhull], True, (255, 0, 0), 3)
        cv2.fillConvexPoly(mask, convexhull, 255)

        face_image_1 = cv2.bitwise_and(img, img, mask=mask)

        # Delaunay triangulation
        rect = cv2.boundingRect(convexhull)
        subdiv = cv2.Subdiv2D(rect)
        subdiv.insert(landmarks_points)
        triangles = subdiv.getTriangleList()
        triangles = np.array(triangles, dtype=np.int32)

        indexes_triangles = []
        for t in triangles:
            pt1 = (t[0], t[1])
            pt2 = (t[2], t[3])
            pt3 = (t[4], t[5])

            index_pt1 = np.where((points == pt1).all(axis=1))
            index_pt1 = extract_index_nparray(index_pt1)

            index_pt2 = np.where((points == pt2).all(axis=1))
            index_pt2 = extract_index_nparray(index_pt2)

            index_pt3 = np.where((points == pt3).all(axis=1))
            index_pt3 = extract_index_nparray(index_pt3)

            if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
                triangle = [index_pt1, index_pt2, index_pt3]
                indexes_triangles.append(triangle)

    frames_array = []
    while True:
        _, img2 = cap.read()
        if img2 is not None:
            # print("🚀 ~ file: views.py ~ line 288 ~ cap.read()", cap.read(),img2)

            img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
            img2_new_face = np.zeros_like(img2)

            # Face 2
            faces2 = detector(img2_gray)
            for face in faces2:
                landmarks = predictor(img2_gray, face)
                landmarks_points2 = []
                for n in range(0, 68):
                    x = landmarks.part(n).x
                    y = landmarks.part(n).y
                    landmarks_points2.append((x, y))

                # cv2.circle(img2, (x, y), 3, (0, 255, 0), -1)
                points2 = np.array(landmarks_points2, np.int32)
                convexhull2 = cv2.convexHull(points2)

            lines_space_mask = np.zeros_like(img_gray)
            lines_space_new_face = np.zeros_like(img2)

            # Triangulation of both faces
            for triangle_index in indexes_triangles:
                # Triangulation of the first face
                tr1_pt1 = landmarks_points[triangle_index[0]]
                tr1_pt2 = landmarks_points[triangle_index[1]]
                tr1_pt3 = landmarks_points[triangle_index[2]]
                triangle1 = np.array([tr1_pt1, tr1_pt2, tr1_pt3], np.int32)

                rect1 = cv2.boundingRect(triangle1)
                (x, y, w, h) = rect1
                cropped_triangle = img[y: y + h, x: x + w]
                cropped_tr1_mask = np.zeros((h, w), np.uint8)

                points = np.array([[tr1_pt1[0] - x, tr1_pt1[1] - y],
                                [tr1_pt2[0] - x, tr1_pt2[1] - y],
                                [tr1_pt3[0] - x, tr1_pt3[1] - y]], np.int32)

                cv2.fillConvexPoly(cropped_tr1_mask, points, 255)

                # Triangulation of second face
                if faces2:
                    tr2_pt1 = landmarks_points2[triangle_index[0]]
                    tr2_pt2 = landmarks_points2[triangle_index[1]]
                    tr2_pt3 = landmarks_points2[triangle_index[2]]
                    triangle2 = np.array([tr2_pt1, tr2_pt2, tr2_pt3], np.int32)

                    rect2 = cv2.boundingRect(triangle2)
                    (x, y, w, h) = rect2

                    cropped_tr2_mask = np.zeros((h, w), np.uint8)

                    points2 = np.array([[tr2_pt1[0] - x, tr2_pt1[1] - y],
                                        [tr2_pt2[0] - x, tr2_pt2[1] - y],
                                        [tr2_pt3[0] - x, tr2_pt3[1] - y]], np.int32)

                    cv2.fillConvexPoly(cropped_tr2_mask, points2, 255)



                    # Warp triangles
                    points = np.float32(points)
                    points2 = np.float32(points2)
                    M = cv2.getAffineTransform(points, points2)
                    warped_triangle = cv2.warpAffine(cropped_triangle, M, (w, h))
                    warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=cropped_tr2_mask)


                    # Reconstructing destination face
                    img2_new_face_rect_area = img2_new_face[y: y + h, x: x + w]
                    img2_new_face_rect_area_gray = cv2.cvtColor(img2_new_face_rect_area, cv2.COLOR_BGR2GRAY)
                    _, mask_triangles_designed = cv2.threshold(img2_new_face_rect_area_gray, 1, 255, cv2.THRESH_BINARY_INV)
                    warped_triangle = cv2.bitwise_and(warped_triangle, warped_triangle, mask=mask_triangles_designed)

                    img2_new_face_rect_area = cv2.add(img2_new_face_rect_area, warped_triangle)
                    img2_new_face[y: y + h, x: x + w] = img2_new_face_rect_area
                else:
                    return HttpResponse("Face not Found")


            # Face swapped (putting 1st face into 2nd face)
            img2_face_mask = np.zeros_like(img2_gray)
            img2_head_mask = cv2.fillConvexPoly(img2_face_mask, convexhull2, 255)
            img2_face_mask = cv2.bitwise_not(img2_head_mask)


            img2_head_noface = cv2.bitwise_and(img2, img2, mask=img2_face_mask)
            result = cv2.add(img2_head_noface, img2_new_face)

            (x, y, w, h) = cv2.boundingRect(convexhull2)
            center_face2 = (int((x + x + w) / 2), int((y + y + h) / 2))

            seamlessclone = cv2.seamlessClone(result, img2, img2_head_mask, center_face2, cv2.MIXED_CLONE)

            cv2.imshow("img2", img2)
            cv2.imshow("clone", seamlessclone)
            cv2.imshow("result", result)
            frames_array.append(seamlessclone)

            if cv2.waitKey(1) & 0xFF == 27:
                break
        else:
            return HttpResponse("Face not captured")

    cap.release()
    cv2.destroyAllWindows()

    video = create_video1("media/", "res", frames_array,
                        frames_array[0].shape[1], frames_array[0].shape[0], 30)
    return render(request,'realtime_face_swapping_webcam.html', {'video':video})

def create_video1(out_dir, video_id, frame_set, frame_w, frame_h, fps=20):
    video_path = os.path.join(out_dir, str(video_id) + '.mp4')
    outWriter = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'),
                                fps, (frame_w, frame_h), True)
    print("🚀 ~ file: views.py ~ line 215 ~ outWriter", type(outWriter))

    print('Saving video...')
    for i in range(len(frame_set)):
        outWriter.write(frame_set[i])
    outWriter.release()
    return video_path

def home(request):
    print("SERVER STARTED")
    return render(request,'index.html')


def image(request,data_image):
    print('Inside image')
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    frame = imutils.resize(frame, width=700)

    # frame = cv2.flip(frame, 1)
    frame= send_face(frame)
    # cv2.imwrite('1.png', frame)
    imgencode = cv2.imencode('.jpg', frame)[1]

    # base64 encode
    stringData = base64.b64encode(imgencode).decode('utf-8')
    b64_src = 'data:image/jpg;base64,'
    stringData = b64_src + stringData

    # emit the frame back
    return render(request,'index.html', {"stringData":stringData})



def test_connect(request):
    print("SOCKET CONNECTED")


def handle_my_custom_event(request):
    print('received my event: '+ str(123))
# cv2.destroyAllWindows()

