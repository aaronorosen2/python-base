from django.shortcuts import render
import uuid
from .models import Parking
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import pdfkit
from json import dumps as jdumps
from django.template.loader import get_template
from django.http import HttpResponse
from django_pdfkit import PDFView
from django.shortcuts import get_object_or_404, render
import os
from django.forms.models import model_to_dict

@csrf_exempt
def new_parking_doc(request):
    if request.POST:        
        parking_doc = Parking()
        parking_doc.id = str(uuid.uuid4())
        try:
            for key, value in dict(request.POST).items():
                setattr(parking_doc, key, request.POST.get(key))
            parking_doc.intake_city_lived = parking_doc.intake_city_lived.split(',')   
            # errors = parking_doc.clean_fields()
            # if not errors:
            parking_doc.save()           
        except Exception as e:
            print(e)
            return JsonResponse({'message': 'failed',
                             'error': str(e)}, status=500)
        return JsonResponse({'message': 'success', 
                             'document_id': parking_doc.id})
@csrf_exempt
def pdf(request, document_id):
    parking_doc = get_object_or_404(Parking, id=document_id)
    if parking_doc and parking_doc is not None:
        setattr(parking_doc,'src',os.path.abspath('./static/parking/img/almeda-logo.png'))
        template_path = 'pdf/parking-pdf-template.html'
        template = get_template(template_path) 
        html = template.render({'data': parking_doc})
        options = {
            'page-size': 'A4',
            'margin-top': '0.5in',
            'margin-right': '0.2in',
            'margin-bottom': '0.5in',
            'margin-left': '0.2in',
            'encoding': "UTF-8",
            "enable-local-file-access": None,   
            "dpi": 150,
            "page-width":"1800px",
            'disable-smart-shrinking': '',
            'zoom':'0.9',
            # 'checkbox-svg': os.path.abspath('./static/pdf_sign/icons/blank-square.svg'),
            # "checkbox-checked-svg": os.path.abspath('./static/pdf_sign/icons/checkbox.svg'),
            # 'enable-forms': '',
            'custom-header' : [
                ('Accept-Encoding', 'gzip')
            ],
            'no-outline': None,
            'load-error-handling':'ignore'
        }
            
        pdf = pdfkit.from_string(html, False, options)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'filename="person.pdf"'
        return response

class  ParkingPDFView(PDFView):
    filename = None
    pdfkit_options = {
         'page-size': 'A4',
         'margin-top': '0.5in',
         'margin-right': '0.3in',
         'margin-bottom': '0.5in',
         'margin-left': '0.3in',
         'encoding': "UTF-8",
         "enable-local-file-access": None,   
         "dpi": 160,
         "page-width":"1800px",
        'disable-smart-shrinking': '',
        # 'enable-forms': '',
        # 'checkbox-svg': os.path.abspath('./static/pdf_sign/icons/blank-square.svg'),
        # "checkbox-checked-svg": os.path.abspath('./static/pdf_sign/icons/checkbox.svg'),
        'zoom':'0.9',
         'custom-header' : [
            ('Accept-Encoding', 'gzip')
         ],
         'no-outline': None,
         'load-error-handling':'ignore'
    }
    def get_context_data(self,*args, **kwargs):
        self.filename = kwargs['document_id']+'.pdf'
        parking_doc = get_object_or_404(Parking, id=kwargs['document_id'])
        setattr(parking_doc,'src',os.path.abspath('./static/parking/img/almeda-logo.png'))
        if parking_doc: return {'data': parking_doc}
        else: return {}


