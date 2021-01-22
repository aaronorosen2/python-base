from django.shortcuts import render, redirect
from .models import Student, Class, ClassEnrolled
from django.contrib.auth.models import User
from django.http.response import JsonResponse,HttpResponseRedirect
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import StudentSerializer, ClassSerializer, ClassEnrolledSerializer
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView



class StudentList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'classroom/students_list.html'

    def get(self, request,*args, **kwargs): 
        return Response({'student_list':Student.objects.all()},template_name = 'classroom/students_list.html')

    def post(self, request, *args, **kwargs):
         
        student_data = Student(name=request.POST['name'],email=request.POST['email'],phone=request.POST['phone']) 
        student_data.save()
        class_ = Class(name=request.POST['class'])
        class_.save()
        class_enrolled = ClassEnrolled(id=None,student=student_data,class_enrolled=class_)
        class_enrolled.save()
        return redirect(request.path)

def delete(request):
    pk = request.GET.get('id',None)
    if pk:
        get_student = Student.objects.get(pk=pk)
        get_student.delete()
        return JsonResponse({'deleted':True})
    return JsonResponse({'deleted':False})

#API for create/delete student to class
@api_view(['GET','POST','DELETE','PUT'])
def studentapi(request):
    if request.method == 'GET':
        serializer = StudentSerializer(Student.objects.all(),many=True)
        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
    
    elif request.method == 'PUT':
        pk = request.GET.get('id')
        if pk:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)
        
    elif request.method == 'DELETE':
        pk = request.GET.get('id')
        if pk:
            try:
                student = Student.objects.get(pk=pk)
                student.delete()
                return JsonResponse(data={"result":True,"success":"Successfully removed student from your class"},status=204)

            except Student.DoesNotExist:
                return JsonResponse(data={"result":False,"error":"Student does not exist on your class"},status=404)
        return JsonResponse(data={"result":False,"error":"Please include student id like ?id=1"},status=400)

@api_view(['GET','POST','DELETE','PUT'])
def classapi(request):
    if request.method == 'GET':
        serializer = ClassSerializer(Class.objects.all(),many=True)

        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        serializer = ClassSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

    elif request.method == 'PUT':
        pk = request.GET.get('id')
        if pk:
            class_ = Class.objects.get(pk=pk)
            serializer = ClassSerializer(class_,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data,status=201)
        return JsonResponse(serializer.errors,status=400)

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
        class_ = Class.objects.get(class_id=request.POST['class'])

        enroll = ClassEnrolled(student=student,class_enrolled=class_)
        enroll.save()
        return JsonResponse(data=request.data,status=200)
