import uuid
from signature.models import Signature
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def set_new_sign(request):
    if request.POST:        
        signature = Signature()
        signature.id = str(uuid.uuid4())
        try:
            signature.sign_data = request.POST.get('sign_data')  
            signature.save()           
        except Exception as e:
            return JsonResponse({'message': 'failed',
                             'error': str(e)}, status=500)
        return JsonResponse({'message': 'success', 
                             'sign_id': signature.id, 'sign_data': signature.sign_data})

