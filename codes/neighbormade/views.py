from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from neighbormade.models import Neighborhood, Stadium
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import NeighborhoodSerializer, StadiumSerializer
import requests
# from bs4 import BeautifulSoup

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


# @api_view(['GET'])
def scrap_stadium(request):
    r = requests.get('https://en.wikipedia.org/wiki/List_of_stadiums_by_capacity')
    html = BeautifulSoup(r.text, 'html.parser')
    stadiums = []
    for table in html.find_all('table'):
        for tbody in table.find_all('tbody'):
            for row in tbody.find_all('tr'):
                cells = row.find_all('td')
                if len(cells)>0:
                    stadium = {}
                    stadium['name'] = cells[0].get_text(strip=True).split('[')[0]
                    stadium['capacity'] = int(process_num(cells[1].get_text(strip=True).split('(')[0].split('[')[0]))
                    statecity = cells[2].get_text(strip=True).split(',')
                    stadium['city'] = statecity[0]
                    stadium['state'] = statecity[1] if len(statecity)>1 else ''
                    stadium['country'] = cells[3].get_text(strip=True)
                    stadium['region'] = cells[4].get_text(strip=True)
                    stadium['teams'] = cells[5].get_text(strip=True)
                    stadium['image'] = ''
                    stadium['sports'] = cells[6].get_text(strip=True) if len(cells)>6 else ''
                    # print(cells[0].find_all('a', href=True)[0]['href'])
                    statium_response = requests.get('https://en.wikipedia.org'+cells[0].find_all('a', href=True)[0]['href'])
                    stdHtml = html = BeautifulSoup(statium_response.text, 'html.parser')
                    Vcard_table = stdHtml.find('table', {'class': 'infobox vcard'})
                    if Vcard_table:
                        Vcard_rows = Vcard_table.find_all('tr')
                        for cardRow in Vcard_rows:
                            img = cardRow.select_one('img')
                            if img:
                                stadium['image'] = 'https:'+img['src']
                                break
                    stadiums.append(Stadium(**stadium))
                    print(len(stadiums), stadium)
            break
        break
    if len(stadiums):
        Stadium.objects.bulk_create(stadiums, 100)
    return JsonResponse({'success': True, 'stadiumsAdded': len(stadiums)})

def get_stadiums(request):
    std = Stadium.objects.all()
    std_serialized = StadiumSerializer(std, many=True)
    return JsonResponse({'stadiums': std_serialized.data})

import re
def process_num(num):
    return float(re.sub(r'[^\w\s.]','',num))