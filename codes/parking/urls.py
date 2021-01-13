from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('<str:document_id>/view', views.pdf),
    path('new_doc', views.new_parking_doc),
    path('print_document/<str:document_id>', views.ParkingPDFView.as_view(template_name='pdf/parking-pdf-template.html'), name='parking-pdf')
]