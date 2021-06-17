from django.shortcuts import render, redirect
from .models import Teacher,Student, Class, InviteClass, ClassEnrolled, ClassEmailAlert, ClassSMSAlert, StudentEmailAlert, StudentSMSAlert, TeacherAccount
from django.contrib.auth.models import User
from django.http.response import JsonResponse,HttpResponseRedirect
from django.http import QueryDict
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import TeacherSerializer,StudentSerializer,UserSerializer, ClassSerializer, ClassEnrolledSerializer, ClassEmailSerializer, ClassSMSSerializer, StudentEmailSerializer, StudentSMSSerializer, InviteLinkSerializer
from knox.auth import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from knox.models import AuthToken
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from form_lead.utils.email_util import send_raw_email
from sfapp2.utils.twilio import send_sms
import json
import uuid
from django.core.validators import validate_email

# teacher api
@api_view(['GET','POST','DELETE','PUT'])
def teacherapi(request):
    if request.method == 'GET' and request.GET.get('teacher'):
        serializer = TeacherSerializer(Teacher.objects.all(),many=True)
        return JsonResponse(serializer.data,safe=False)
        
    if request.method == "GET":
        serializer = UserSerializer(User.objects.all(),many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == "POST":
        teacher = User.objects.get(id=request.data.get('teacher'))
        student = Student.objects.get(id=request.data.get('student'))
        teacher = Teacher(teacher=teacher,student=student)
        teacher.save()
        return JsonResponse({"Result":True},status=201)

    elif request.method == "DELETE":
        tid = request.GET.get('tid')
        sid = request.GET.get('sid')
        try:
            student = Teacher.objects.get(student_id=sid,teacher_id=tid)
            student.delete()
            return JsonResponse(data={"result":True,"success":"Successfully removed student from teacher"},status=204)
            
        except Teacher.DoesNotExist:
            return JsonResponse(data={"result":False,"error":"Teacher-Student does not exist"},status=404)

#API for create/delete student to class
@api_view(['GET','POST','DELETE','PUT'])
def studentapi(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])

    if request.method == 'GET' and request.GET.get('teacher'):
        serializer = StudentSerializer(Student.objects.all(),many=True)
        return JsonResponse(serializer.data,safe=False)
             
    elif request.method == 'GET':
        serializer = StudentSerializer(Student.objects.filter(user_id=token.user_id),many=True)
        return JsonResponse(serializer.data,safe=False)
    
    elif request.method == 'POST':
        try:
            user = User.objects.get(id=token.user_id)
            student = Student(name=request.data['name'],email=request.data['email'],phone=request.data['phone'],user=user)
            student.save()
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)
    
    elif request.method == 'PUT':
        try:
            student = Student.objects.get(pk=request.data['id'])
            user = User.objects.get(id=token.user_id)
            student.name = request.data['name']
            student.email = request.data['email']
            student.phone = request.data['phone']
            student.user = user
            student.save() 
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)
        
    elif request.method == 'DELETE':
        pk = request.GET.get('id')
        if pk:
            try:
                student = Student.objects.get(pk=pk)
                student.delete()
                return JsonResponse(data={"success":True,"message":"Successfully removed student from your class"},status=204)

            except Student.DoesNotExist:
                return JsonResponse(data={"success":False,"message":"Student does not exist on your class"},status=404)
        return JsonResponse(data={"success":False,"message":"Please include student id like ?id=1"},status=400)



@api_view(['GET','POST','DELETE','PUT'])
def classapi(request):
    token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])
    if request.method == 'GET':
        serializer = ClassSerializer(Class.objects.filter(user_id=token.user_id),many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        try:
            user = User.objects.get(id=token.user_id)
            class_ = Class(class_name=request.data['class_name'],user=user)
            class_.save()
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)

    elif request.method == 'PUT':
        try:
            user = User.objects.get(id=token.user_id)
            class_ = Class.objects.get(pk=request.data['id'])
            class_.class_name = request.data['class_name']
            class_.user = user
            class_.save()
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)

    elif request.method == 'DELETE':
        pk = request.GET.get('id')
        if pk:
            try:
                class_ = Class.objects.get(pk=pk)
                class_.delete()
                return JsonResponse(data={"result":True,"success":"Successfully removed class from your list"},status=204)

            except Class.DoesNotExist:
                return JsonResponse(data={"result":False,"error":"Class does not exist"},status=404)
        return JsonResponse(data={"result":False,"error":"Please include class id like ?id=1"},status=400)

@api_view(['GET','POST','DELETE','PUT'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def classenrolledapi(request):

    if request.method == 'GET':
        serializer = ClassEnrolledSerializer(ClassEnrolled.objects.filter(class_enrolled__in=Class.objects.filter(user=request.user)),many=True)
        
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'DELETE':
        cid = request.GET.get('cid')
        sid = request.GET.get('sid')
        try:
            student = ClassEnrolled.objects.get(student_id=sid,class_enrolled_id=cid)
            student.delete()
            return JsonResponse(data={"result":True,"success":"Successfully removed class from your list"},status=204)
        except ClassEnrolled.DoesNotExist:
            return JsonResponse(data={"result":False,"error":"Class does not exist"},status=404)
        return JsonResponse(data={"result":False,"error":"Please include class id like ?id=1"},status=400)
    
    elif request.method == 'POST':
        student = Student.objects.get(name=request.POST['student'])
        class_ = Class.objects.get(id=request.POST['class'])

        enroll = ClassEnrolled(student=student,class_enrolled=class_)
        enroll.save()
        return JsonResponse(data=request.data,status=200)

@csrf_exempt
@api_view(['GET','POST'])
def send_mail(request):
    if request.method == "POST":
        emails = []
        for enroll in ClassEnrolled.objects.filter(class_enrolled_id=request.POST['class_enrolled_id']):
            emails.append(enroll.student.email)
            student = QueryDict('', mutable=True)
            student.update({"student_id":enroll.student.id,"message":request.POST['message']})
            serializer = StudentEmailSerializer(data=student)
            if serializer.is_valid():
                serializer.save()

        subject = request.POST['message'].split("\n")[0]
        body = "\n".join(request.POST['message'].split("\n")[1:])
        send_raw_email(to_email=emails,reply_to=None,
                        subject=subject,
                        message_text=body,
                        message_html=None)

        serializer = ClassEmailSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors,status=404)

    elif request.method == "GET":
        serializer = ClassEmailSerializer(ClassEmailAlert.objects.all(),many=True)
        
        return JsonResponse(serializer.data,safe=False)


@api_view(['GET'])
def student_mail(request):

    if request.method == 'GET':
        serializer = StudentEmailSerializer(StudentEmailAlert.objects.all(), many=True)
        return JsonResponse(serializer.data,safe=False)
    

@csrf_exempt
@api_view(['GET','POST'])
def send_text(request):

    if request.method == 'POST':
        for enroll in ClassEnrolled.objects.filter(class_enrolled_id = request.POST['class_enrolled_id']):
            st_qdict = QueryDict("",mutable=True)
            st_qdict.update({"student_id":enroll.student.id,"message":request.POST['message']})
            send_sms(to_number=enroll.student.phone,body=request.POST['message'])
            serializer = StudentSMSSerializer(data=st_qdict)
            if serializer.is_valid():
                serializer.save()

        serializer = ClassSMSSerializer(data=request.POST)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=200)
        return JsonResponse(serializer.errors,status=404)

    if request.method == 'GET':
        serializer = ClassSMSSerializer(ClassSMSAlert.objects.all(),many=True)
        return JsonResponse(serializer.data,safe=False)

@api_view(['GET'])
def student_text(request):
    serializer = StudentSMSSerializer(StudentSMSAlert.objects.all(),many=True)
    return JsonResponse(serializer.data, safe=False)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_invitation_link(request):
    invite = InviteClass.objects.get(class_invited_id=Class.objects.get(id=request.GET.get('class_id')))
    if invite and invite is not None:
        invite = InviteLinkSerializer(invite).data
        return JsonResponse({'uuid': invite['uuid'], 'class_id': invite['class_invited']['id']}, safe=False)
    else:
        invite = InviteClass(class_invited_id=request.GET.get('class_id'), uuid= str(uuid.uuid4()))
        invite.save()
        invite = InviteLinkSerializer(invite).data
        return JsonResponse({'uuid': invite['uuid'], 'class_id': invite['class_invited']['id']})

@csrf_exempt
def get_invitation_info(request):
    invite = InviteClass.objects.filter(class_invited_id=Class.objects.get(id=request.GET.get('class_id'))).first()
    if invite and invite is not None:
        invite = InviteLinkSerializer(invite).data
        return JsonResponse(invite, safe=False)

@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def joinClass(request):
    if request.POST.get('phone') and request.POST.get('class_id') and request.POST.get('name') and isValidEmail(request.POST.get('email')):
        try:
            class_ = Class.objects.get(id=request.POST['class_id'])
            if class_ is not None:
                student = Student.objects.filter(email=request.POST.get('email'),user=class_.user).first()
                if student is None:
                    student = Student(name=request.POST.get('name'),email=request.POST.get('email'),phone=request.data.get('phone'),user=class_.user)
                    student.save()
                enroll_exists = ClassEnrolled.objects.filter(student=student,class_enrolled=class_).first()
                if enroll_exists is not None:
                    return JsonResponse({'success': False,'msg': 'Already enrolled!'},status=409)
                enroll = ClassEnrolled(student=student,class_enrolled=class_)
                enroll.save()
                return JsonResponse({"success":True},status=201)
        except Exception as e:
            # print(e)
            return JsonResponse({"success":False},status=400)
    return JsonResponse({"success":False, 'msg': 'Invalid parameters'},status=422)

def isValidEmail(email):
    try:
        validate_email(email)
        return True
    except Exception as e:
        print(e)
        return False


@api_view(['POST'])
@csrf_exempt
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def setTeacherStatus(request):
    if isinstance(request.data.get('status'), bool):
        try:
            t_acc, created = TeacherAccount.objects.update_or_create(teacher_id=request.data.get('userId'),defaults={'active':request.data.get('status')})
            return JsonResponse({"success":True},status=201)
        except Exception as e:
            print(e)
            return JsonResponse({"success":False},status=400)
    return JsonResponse({"success":False, 'msg': 'Invalid parameters'},status=422)