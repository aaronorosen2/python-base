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

#API for create/delete student to class
@api_view(['GET','POST','DELETE'])
def studentlist(request):
    if request.method == 'GET':
        students = Student.objects.all()
        serializer = StudentSerializer(students,many=True)

        return JsonResponse(serializer.data,safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = StudentSerializer(data=data)
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
        return JsonResponse(data={"result":False,"error":"Please include student id"},status=400)
        