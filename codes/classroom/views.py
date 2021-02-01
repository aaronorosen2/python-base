from django.shortcuts import render, redirect
from .models import Student, Class, ClassEnrolled, ClassEmailAlert, ClassSMSAlert, StudentEmailAlert, StudentSMSAlert
from django.contrib.auth.models import User
from django.http.response import JsonResponse,HttpResponseRedirect
from django.http import QueryDict
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import StudentSerializer, ClassSerializer, ClassEnrolledSerializer, ClassEmailSerializer, ClassSMSSerializer, StudentEmailSerializer, StudentSMSSerializer
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from form_lead.utils.email_util import send_raw_email
from sfapp2.utils.twilio import send_sms
import json
#API for create/delete student to class
@api_view(['GET','POST','DELETE','PUT'])
def studentapi(request):
    if request.method == 'GET':
        serializer = StudentSerializer(Student.objects.all(),many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        try:
            user = User.objects.get(username=request.data.get('user'))
            student = Student(name=request.data['name'],email=request.data['email'],phone=request.data['phone'],user=user)
            student.save()
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)
    
    elif request.method == 'PUT':
        pk = request.GET.get('id')
        if pk:
            student = Student.objects.get(pk=pk)
            user = User.objects.get(username=request.data['user'])
            student.name = request.data['name']
            student.email = request.data['email']
            student.phone = request.data['phone']
            student.user = user
            student.save()
            return JsonResponse({"success":True},status=201)
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
    if request.method == 'GET':
        serializer = ClassSerializer(Class.objects.all(),many=True)

        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        try:
            user = User.objects.get(username=request.data['user'])
            class_ = Class(class_name=request.data['class_name'],user=user)
            class_.save()
            return JsonResponse({"success":True},status=201)
        except:
            return JsonResponse({"success":False},status=400)

    elif request.method == 'PUT':
        try:
            user = User.objects.get(username=request.data['user'])
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
def classenrolledapi(request):

    if request.method == 'GET':

        serializer = ClassEnrolledSerializer(ClassEnrolled.objects.all(),many=True)
        
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