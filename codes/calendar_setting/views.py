from django.shortcuts import render

# Create your views here.
from rest_framework.generics import (ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.response import Response

from . import models ,serializers


class CalendarSettingApi(ListCreateAPIView):
    queryset = models.CalendarSetting.objects.all()
    serializer_class = serializers.CalendarSettingSerializers

    def create(self , request , *args , **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        # headers = self.get_success_headers(serializer.data)
        instance = serializer.save()
        return Response(serializer.data)


class CalendarSingleOperationApi(RetrieveUpdateDestroyAPIView):
    
    serializer_class = serializers.CalendarSettingDetailsSerializers

    def get_queryset(self):
        return models.EmployeesLeave.objects.filter(id=self.kwargs.get('pk', None))

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
                # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}
        return Response({"status": True, "message": "Schedule Updated !", "data": serializer.data})

    def delete(self, request, *args, **kwargs):
        if self.destroy(request, *args, **kwargs):
            return Response({"message": "Schedule Cancel !"})
        else:
            return Response({"message" : "Schedule  Not Found"})
