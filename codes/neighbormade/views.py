from django.shortcuts import render
import pandas as pd
from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from neighbormade.models import Neighborhood, Stadium,Subreddit
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import NeighborhoodSerializer, StadiumSerializer, SubredditSerializer
import requests
import praw
import re
from datetime import datetime
from uszipcode.search import SearchEngine

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


def importNbrWithZip(request):
    search = SearchEngine()
    states = ["Alabama", "Arkansas", "California", "Colorado", "Florida", "Georgia", "Illinois", "Indiana", "Iowa", "Kentucky", "Louisiana", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Missouri", "Nebraska", "New York", "North Carolina", "North Dakota", "Ohio", "Oregon", "Pennsylvania", "Tennessee", "Texas", "Utah", "Virginia", "Washington", "Washington State", "Wisconsin","Alaska","Hawaii","Arizona","New Jersey","Montana","Maine","Nevada","Connecticut","New Maxico","Mississippi","South Carolina","Kansas","Delaware","Wyoming","Idaho","Rhode Island","Vermont","West Virginia","South Dakota","New Hampshire","Oklahoma"]
    totalImported = 0
    states = list(set(states))
    for state in states:
        hoodsInState = []
        stateData = search.by_state(state, zipcode_type='Standard', sort_by='zipcode', ascending=True, returns=50000)
        for zipcode in stateData:
            hoodsInState.append(Neighborhood(
                zipcode = zipcode.zipcode,
                state = state,
                city = zipcode.major_city, 
                latitude = zipcode.lat,
                longitude = zipcode.lng)
                )
        if len(hoodsInState):
            print(state)
            try:
                Neighborhood.objects.bulk_create(hoodsInState, 100)
            except Exception as e:
                print(e)            
            totalImported += len(hoodsInState)
            print('imported ', len(hoodsInState), 'zipcodes from -', state)
        print('total imported:', totalImported)
    return JsonResponse({'Total zipcodes imported': totalImported})

def viewNeighbours(request):
    nbr = Neighborhood.objects.all()
    nbr_serialized = NeighborhoodSerializer(nbr, many=True)
    return JsonResponse({'nbr': nbr_serialized.data})

@api_view(['GET'])
def get_states(request):
    # if request.user.is_authenticated:
    states = Neighborhood.objects.values_list('state', flat=True).distinct().order_by('state')
    state_serialized = list(states)
    # state_serialized.sort()
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
    hoods = Neighborhood.objects.filter(state=state, city=city).values('name', 'id').distinct()
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


def process_num(num):
    return float(re.sub(r'[^\w\s.]','',num))

def scrap_reddits(request):
    reddit = praw.Reddit(client_id='cD81gYCeIEjByA', client_secret='_DF466jhZte3SsUnClhvN2DGtctKrQ', user_agent='scrapper')
    posts = []
    hot_posts = reddit.subreddit('all').hot(limit=None)
    for post in hot_posts:
        _post = {}
        _post['title'] = post.title.strip()
        _post['score'] = post.score
        _post['subreddit'] = str(post.subreddit)
        _post['url'] = post.url
        _post['body'] = post.selftext.strip()
        _post['reddit_post_id'] = post.id
        _post['num_comments'] = post.num_comments
        _post['created_at'] = str(datetime.utcfromtimestamp(post.created))
        _post['upvote_ratio'] = post.upvote_ratio
        # rows = Subreddit.objects.filter(reddit_post_id=post.id).update(**_post)
        # if rows == 0:
        posts.append(Subreddit(**_post))
        print(len(posts))
        print(str(_post))
    if len(posts):
        # Subreddit.objects.all().delete()
        Subreddit.objects.bulk_create(posts, 100)
    # posts = pd.DataFrame(posts,columns=['title', 'score', 'id', 'subreddit', 'url', 'num_comments', 'body', 'created', 'upvote_ratio'])
    return JsonResponse({'success': True,'posts_fetched':len(posts)})

def get_reddit_posts(request):
    std = Subreddit.objects.all().distinct()
    std_serialized = SubredditSerializer(std, many=True)
    return JsonResponse({'posts': std_serialized.data, 'total': len(std_serialized.data)})

def get_subreddits(request):
    srd = Subreddit.objects.values_list('subreddit', flat=True).distinct()
    srd_serialized = list(srd)
    return JsonResponse({'subreddits': srd_serialized, 'total': len(srd_serialized)})
