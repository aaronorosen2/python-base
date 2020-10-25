import uuid
from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from sfapp2.utils.twilio import send_confirmation_code
from django.views.decorators.csrf import csrf_exempt
from sfapp2.models import Member, Token, Upload, Service


@csrf_exempt
def get_services(request):
    services = Service.objects.filter().all()
    datas = []
    for service in services:
        datas.append({
            'title': service.title,
            'description': service.description,
            'phone': service.phone,
            'latitude': float(service.latitude),
            'longitude':  float(service.longitude),
        })
    print(datas)
    return JsonResponse(datas, safe=False)


@csrf_exempt
def confirm_phone_number(request):
    if not request.POST:
        raise Http404()

    phone_number = request.POST.get('phone_number')
    if not phone_number:
        return JsonResponse({'message': 'Phone number is required'})

    member = Member.objects.filter(phone=phone_number).first()
    if not member:
        member = Member()
        member.phone = phone_number

    member.code_2fa = send_confirmation_code(phone_number)
    member.save()

    return JsonResponse({'message': '2fa pending'})


@csrf_exempt
def verify_2fa(request):
    if request.POST:
        code = request.POST.get('code_2fa')
        phone = request.POST.get('phone_number')
        member = Member.objects.filter(phone=phone).first()
        if not member:
            return JsonResponse({'message': 'Error'})

        if member.code_2fa and member.code_2fa == code:
            member.has_verified_phone = True
            # clear code_2fa after use
            member.code_2fa = ''
            member.save()
            neighbormade_token = Token()
            neighbormade_token.member = member
            neighbormade_token.token = str(uuid.uuid4())
            neighbormade_token.save()

            return JsonResponse({'message': 'success',
                                 'token': neighbormade_token.token})
        else:
            return JsonResponse({'message': 'invalid_code'})


def get_member_from_headers(headers):
    token = headers.get("Authorization")
    if token:
        user_token = Token.objects.filter(
            token=token).first()
        if user_token:
            return user_token.member


@csrf_exempt
def test_login(request):
    return render(request, 'test/login.html')


@csrf_exempt
def test_store(request):
    return render(request, 'test/store.html')


@csrf_exempt
def test_product(request):
    return render(request, 'test/product.html')
