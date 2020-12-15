from django.shortcuts import get_object_or_404, render
import time
import json
import uuid
from django.http import Http404, HttpResponseBadRequest
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Doc
import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.views.generic import ListView
import pdfkit
from django_pdfkit import PDFView
# Create your views here.

@csrf_exempt
def set_document_text(request):
    if request.POST:        
        pdf_doc = Doc()
        pdf_doc.document_id = str(uuid.uuid4())
        for key, value in dict(request.POST).items():
            setattr(pdf_doc, key, request.POST.get(key))
        pdf_doc.listing_firm_commission = int(request.POST.get('listing_firm_comm'))
        pdf_doc.selling_firm_commission = int(request.POST.get('selling_firm_comm'))
        pdf_doc.is_seller = True if pdf_doc.is_seller else False
        pdf_doc.is_buyer = True if pdf_doc.is_buyer else False
        try:
            errors = pdf_doc.clean_fields()
            print(errors)
            if not errors:
                pdf_doc.save()
        except Exception as e:
            return JsonResponse({'message': 'failed',
                             'error': str(e)}, status=500)
        return JsonResponse({'message': 'success', 
                             'document_id': pdf_doc.document_id})
        
@csrf_exempt
def save_referring_signature(request, document_id):
    if request.POST:        
        pdf_doc = Doc.objects.filter(document_id=document_id).first()
        if pdf_doc:            
            pdf_doc.ref_sign = request.POST.get('sign')            
            try:   
                errors = pdf_doc.clean_fields()
                print(errors)
                if not errors:
                    pdf_doc.save()
            except Exception as e:
                return JsonResponse({'message': 'failed',
                                'error': str(e)},status=500)
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'failed',
                                'error': 'Docment not found'})

@csrf_exempt
def save_destination_signature(request, document_id):
     if request.POST:        
        pdf_doc = Doc.objects.filter(document_id=document_id).first()
        if pdf_doc:            
            pdf_doc.dest_sign = request.POST.get('sign')            
            try:   
                errors = pdf_doc.clean_fields()
                print(errors)
                if not errors:
                    pdf_doc.save()
            except Exception as e:
                return JsonResponse({'message': 'failed','error': str(e)},status=500)
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'failed',
                                'error': 'Docment not found'})
            
@csrf_exempt
def save_and_print(request, document_id):
     if request.POST:        
        pdf_doc = Doc.objects.filter(phone=document_id).first()
        if pdf_doc:            
            pdf_doc.dest_sign = request.POST.get('ref_sign')            
            try:   
                errors = pdf_doc.clean_fields()
                print(errors)
                if not errors:
                    pdf_doc.save()
            except Exception as e:
                return JsonResponse({'message': 'failed','error': str(e)})
            return JsonResponse({'message': 'success'})
        else:
            return JsonResponse({'message': 'failed',
                                'error': 'Docment not found'})
            
def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path
    
@csrf_exempt
def render_pdf_view(request, document_id):
    # if request.GET:
    pdf_doc = get_object_or_404(Doc, document_id=document_id)
    if pdf_doc:
        try:            
            template_path = 'pdf/pdf-template.html'
            context = pdf_doc
            # Create a Django response object, and specify content_type as pdf
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'filename="report.pdf"'
            # find the template and render it.
            template = get_template(template_path)
            
            html = template.render({'data': context})
            # return render(request,template_path)
            # create a pdf
            pisa_status = pisa.CreatePDF(
            html, dest=response, link_callback=link_callback)
            # if error then show some funy view
            if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
            return response
        except Exception as e:
            return JsonResponse({'message': 'failed',
                        'error': str(e)})
    else:
        return JsonResponse({'message': 'failed',
                        'error': 'Docment not found'})
        
def pdf(request, document_id):
    pdf_doc = get_object_or_404(Doc, document_id=document_id)
    template_path = 'pdf/pdf-template.html'
    template = get_template(template_path)            
    html = template.render({'data': pdf_doc})
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
        
    pdf = pdfkit.from_string(html, False, options)
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="person.pdf"'
    return response


class  SFAppPDFView(PDFView):
    filename = None
    pdfkit_options = {
         'page-size': 'A4',
         'margin-top': '0.5in',
         'margin-right': '1in',
         'margin-bottom': '0.5in',
         'margin-left': '1in',
         'encoding': "UTF-8",
         "enable-local-file-access": '',   
         "dpi": 400,
        #  "page-width":"1536px",
        'disable-smart-shrinking': '',
        # 'enable-forms': '',
         'custom-header' : [
            ('Accept-Encoding', 'gzip')
         ],
         'no-outline': None,
         'load-error-handling':'ignore'
    }
    def get_context_data(self,*args, **kwargs):
        self.filename = kwargs['document_id']+'.pdf'
        pdf_doc = get_object_or_404(Doc, document_id=kwargs['document_id'])
        print(pdf_doc)
        if pdf_doc: return {'data': pdf_doc}
        else: return {}



