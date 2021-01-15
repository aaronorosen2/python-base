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
         
        student_data = Student(name=request.POST['name'],email=request.POST['email'],phone=request.POST['phone']) 
        student_data.save()
        student_list = Student.objects.all()
        return Response({'student_list':student_list},template_name = 'classroom/students_list.html')

def delete(request):
    pk = request.GET.get('id',None)
    if pk:
        get_student = Student.objects.get(pk=pk)
        get_student.delete()
        return JsonResponse({'deleted':True})
    return JsonResponse({'deleted':False})

