from django.urls import path
from django_pdfkit import PDFView
from . import views
from django.conf import settings
from django.conf.urls.static import static
options = {
         'page-size': 'A4',
         'margin-top': '0.5in',
         'margin-right': '1in',
         'margin-bottom': '0.5in',
         'margin-left': '1in',
         'encoding': "UTF-8",
         "enable-local-file-access": None,   
         "dpi": 400,
        #  "page-width":"1536px",
        'disable-smart-shrinking': '',
        # 'enable-forms': '',
         'custom-header' : [
            ('Accept-Encoding', 'gzip')
         ],
         'no-outline': None,
    }

urlpatterns = [
    path('set_document_text', views.set_document_text),
    path('sign_document/<str:document_id>/signature1', views.save_referring_signature),
    path('sign_document/<str:document_id>/signature2', views.save_destination_signature),
    path('sign_document/<str:document_id>/print', views.pdf),
    path('sign_document/<str:document_id>/view_as_pdf', views.SFAppPDFView.as_view(template_name='pdf/pdf-template.html'), name='sfapp-pdf')
]
