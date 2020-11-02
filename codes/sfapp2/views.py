import time
import json
import uuid
from django.shortcuts import render
from django.http import Http404, HttpResponseBadRequest
from django.http import JsonResponse
from sfapp2.utils.twilio import send_confirmation_code
from django.views.decorators.csrf import csrf_exempt
from sfapp2.models import Member, Token, Upload, Service, GpsCheckin


def to_list(el):
    if not el:
        return []
    return [s for s in json.loads(el)]


@csrf_exempt
def get_services(request):
    services = Service.objects.filter().all()
    datas = []
    population_types = []
    service_types = []
    for service in services:

        service_types += to_list(service.services_list)
        population_types += to_list(service.population_list)

        print(to_list(service.services_list))
        datas.append({
            'title': service.title,
            'description': service.description,
            'address': service.address,
            'phone': service.phone,
            'latitude': float(service.latitude),
            'longitude':  float(service.longitude),
            'services':  service.services,
            'other_info': service.other_info,
            'services_list': to_list(service.services_list),
            'population_list': to_list(service.population_list),
        })

    service_types = list(set(service_types))
    population_types = list(set(population_types))
    service_types.sort()
    population_types.sort()
    results = {
        'places': datas,
        'service_types': service_types,
        'population_types': population_types,
    }
    return JsonResponse(results, safe=False)


@csrf_exempt
def confirm_phone_number(request):
    if not request.POST:
        raise Http404()

    phone_number = request.POST.get('phone_number')
    if not phone_number:
        raise HttpResponseBadRequest()

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
            raise HttpResponseBadRequest()

        if member.code_2fa and member.code_2fa == code:
            member.has_verified_phone = True
            # clear code_2fa after use
            member.code_2fa = ''
            member.save()
            token = Token()
            token.member = member
            token.token = str(uuid.uuid4())
            token.save()

            return JsonResponse({'message': 'success',
                                 'token': token.token})
        else:
            raise HttpResponseBadRequest()


def get_member_from_headers(headers):
    token = headers.get("Authorization")
    if token:
        user_token = Token.objects.filter(
            token=token).first()
        if user_token:
            return user_token.member

@csrf_exempt
def set_user_info(request):
    if request.POST:
        name = request.POST.get('name')
        member = get_member_from_headers(request.headers)
        if name and member:
            print("SAVE NAME!!")
            member.name = name
            member.save()

        return JsonResponse({'message': 'success'})

@csrf_exempt
def do_checkin_gps(request):
    if request.POST:
        msg = request.POST.get('msg')
        member = get_member_from_headers(request.headers)
        if msg and member:
            gps_checkin = GpsCheckin()
            gps_checkin.member = member
            gps_checkin.msg = request.POST.get("msg", "")
            gps_checkin.lat = request.POST.get("lat", "")
            gps_checkin.lng = request.POST.get("lng", "")
            gps_checkin.save()

        return JsonResponse({'message': 'success'})

@csrf_exempt
def checkin_activity(request):
    member = get_member_from_headers(request.headers)
    if member:
        gps_checkins = GpsCheckin.objects.filter(
            member=member).order_by('-created_at').all()
        events = []
        for gps_checkin in gps_checkins:
            t = gps_checkin.created_at
            events.append({
                'type': 'gps',
                'lat': gps_checkin.lat,
                'lng': gps_checkin.lng,
                'msg': gps_checkin.msg,
                'created_at': time.mktime(t.timetuple()),
            })
        return JsonResponse({'events': events})


@csrf_exempt
def test_login(request):
    return render(request, 'test/login.html')


@csrf_exempt
def test_store(request):
    return render(request, 'test/store.html')


@csrf_exempt
def test_product(request):
    return render(request, 'test/product.html')