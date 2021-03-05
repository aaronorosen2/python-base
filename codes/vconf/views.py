from django.shortcuts import render
from vconf.models import Categories
from .serializers import CategoriesSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.response import Response

# Create your views here.


@method_decorator(csrf_exempt, name='dispatch')
class UploadCategory(generics.ListCreateAPIView):
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer

    def post(self, request, *args, **kwargs):
        try:
            try:
                category = Categories.objects.get(
                    category=request.data['category'].capitalize())
                return Response({"error": "Brand Already Exists!"}, status=400)
            except Categories.DoesNotExist:
                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                category = serializer.save()
                return Response({
                    "category": CategoriesSerializer(category, context=self.get_serializer_context()).data
                })
        except Exception as ex:
            return Response({
                "error": str(ex)
            }, status=400)
