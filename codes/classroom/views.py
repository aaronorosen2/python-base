from django.shortcuts import render
from .models import Student
from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
from .serializers import StudentSerializer
from rest_framework.decorators import api_view
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView



class StudentList(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'classroom/students_list.html'

    def get(self, request,*args, **kwargs):
        student_list = Student.objects.all()
        return Response({'student_list':student_list},template_name = 'classroom/students_list.html')

    def post(self, request, *args, **kwargs):
         
        student_data= Student(name=request.POST['name'],email=request.POST['email'],phone=request.POST['phone']) 
        student_data.save()
        student_list = Student.objects.all()
        return Response({'student_list':student_list},template_name = 'classroom/students_list.html')

# @api_view(http_method_names=['GET','POST','DELETE'])
# def get_students_list(request):
#     if request.method == 'GET':
        
#         return render(request,'classroom/students_list.html',{'student_list':student_list})

