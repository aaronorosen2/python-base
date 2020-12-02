from django.core.files import File
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import LessonSerializer
from .models import Lesson
import json
import uuid

@api_view(['GET'])
def apiOverview(request):
    return Response("Hey There")

# Lesson API Start

@api_view(['POST'])
def lesson_create(request):
    database_data = ""
    with open("db.json","r") as db:
        database_data = json.load(db)

    with open("db.json","w") as db:
        database_data[str(uuid.uuid4())] = request.data
        json.dump(database_data,db)
        return Response("Created")


@api_view(['GET'])
def lesson_read(request,pk):
    with open("db.json","r") as db:
        data_json = json.load(db)
        return Response(data_json[pk])

@api_view(['POST'])
def lesson_update(request,pk):
    database_data = ""

    with open("db.json","r") as db:
        database_data = json.load(db)

    with open("db.json","w") as db:
        database_data[pk] = request.data
        json.dump(database_data,db)
        return Response("Updated")

@api_view(['DELETE'])
def lesson_delete(request,pk):
    database_data = ""
    with open("db.json","r") as db:
        database_data = json.load(db)

    del database_data[pk]
    with open("db.json","w") as db:
        json.dump(database_data,db)
        return Response("Deleted")

# Flashcard API Start

@api_view(['POST'])
def flashcard_create(request,lessonId):
    database_data = {}
    lesson_data = {}
    with open("db.json","r") as db:
        database_data = json.load(db)
        lesson_data = database_data[lessonId]

    with open("db.json","w") as db:
        lesson_data.append(request.data)
        database_data[lessonId] = lesson_data
        json.dump(database_data,db)
        return Response("Flashcard Created")

@api_view(['GET'])
def flashcard_read(request,lessonId,pk):

    with open("db.json","r") as db:
        database_data = json.load(db)
        lesson_data = database_data[lessonId]
        flashcard_data = lesson_data[pk]
        return Response(flashcard_data)

@api_view(['POST'])
def flashcard_update(request,lessonId,pk):
    with open("db.json","r") as db:
        database_data = json.load(db)
        lesson_data = database_data[lessonId]
        flashcard_data = request.data
        
    with open("db.json","w") as db:
        lesson_data[pk] = flashcard_data
        database_data[lessonId] = lesson_data
        json.dump(database_data,db)
        return Response("Flashcard updated")

@api_view(['DELETE'])
def flashcard_delete(request,lessonId,pk):
    with open("db.json","r") as db:
        database_data = json.load(db)
        lesson_data = database_data[lessonId]
        del lesson_data[pk]

    with open("db.json","w") as db:
        database_data[lessonId] = lesson_data
        json.dump(database_data,db)
        return Response("Flashcard deleted")