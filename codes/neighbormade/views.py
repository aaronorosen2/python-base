from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from neighbormade.models import Neighborhood
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import NeighborhoodSerializer

# Create your views here.
def importNeighbours(request):
    Neighborhood.objects.all().delete()
    df = pd.read_csv('neighbormade/US Neighborhood List - Sheet1.csv', sep=',')
    df.drop(df.columns[[0]], axis=1, inplace=True)
    hoods = list()
    for row in df:
        splitted = row.split('-')
        city = splitted[0].strip()
        state = splitted[1].strip()
        latlong = row.split('(')[1].strip()[0:-1].split(',')
        lat = float(latlong[0].strip())
        longitude = float(latlong[1].strip())
        for hood in df[row]:
            if pd.notna(hood):
                hoods.append(Neighborhood(
                name = hood.strip(),
                state = state,
                city = city,
                latitude = lat,
                longitude = longitude)
                )
    if len(hoods):
        Neighborhood.objects.bulk_create(hoods, 100)
    return JsonResponse({'success': True, 'hoodsAdded': len(hoods)})

def viewNeighbours(request):
    nbr = Neighborhood.objects.all()
    nbr_serialized = NeighborhoodSerializer(nbr, many=True)
    return JsonResponse({'nbr': nbr_serialized.data})

@api_view(['GET'])
def get_states(request):
    # if request.user.is_authenticated:
    states = Neighborhood.objects.values_list('state', flat=True).distinct()
    state_serialized = list(states)
    return JsonResponse({'states':state_serialized})

@api_view(['GET'])
def get_cities(request, state):
    # if request.user.is_authenticated:
    cities = Neighborhood.objects.filter(state=state).values_list('city', flat=True).distinct()
    city_serialized = list(cities)
    return JsonResponse({'cities':city_serialized})

@api_view(['GET'])
def get_hoods(request, state, city):
    # if request.user.is_authenticated:
    hoods = Neighborhood.objects.filter(state=state, city=city).values_list('name', flat=True).distinct()
    hoods_serialized = list(hoods)
    return JsonResponse({'hoods':hoods_serialized})









    # token = AuthToken.objects.get(token_key = request.headers.get('Authorization')[:8])

    # if request.method == 'GET' and request.GET.get('teacher'):
    #     serializer = StudentSerializer(Student.objects.all(),many=True)
    #     return JsonResponse(serializer.data,safe=False)
             
    # elif request.method == 'GET':
    #     serializer = StudentSerializer(Student.objects.filter(user_id=token.user_id),many=True)
    #     return JsonResponse(serializer.data,safe=False)
    
    # elif request.method == 'POST':
    #     try:
    #         user = User.objects.get(id=token.user_id)
    #         student = Student(name=request.data['name'],email=request.data['email'],phone=request.data['phone'],user=user)
    #         student.save()
    #         return JsonResponse({"success":True},status=201)
    #     except:
    #         return JsonResponse({"success":False},status=400)
    
    # elif request.method == 'PUT':
    #     try:
    #         student = Student.objects.get(pk=request.data['id'])
    #         user = User.objects.get(id=token.user_id)
    #         student.name = request.data['name']
    #         student.email = request.data['email']
    #         student.phone = request.data['phone']
    #         student.user = user
    #         student.save() 
    #         return JsonResponse({"success":True},status=201)
    #     except:
    #         return JsonResponse({"success":False},status=400)
        
    # elif request.method == 'DELETE':
    #     pk = request.GET.get('id')
    #     if pk:
    #         try:
    #             student = Student.objects.get(pk=pk)
    #             student.delete()
    #             return JsonResponse(data={"success":True,"message":"Successfully removed student from your class"},status=204)

    #         except Student.DoesNotExist:
    #             return JsonResponse(data={"success":False,"message":"Student does not exist on your class"},status=404)
    #     return JsonResponse(data={"success":False,"message":"Please include student id like ?id=1"},status=400)
