import uuid
from django.shortcuts import render
from django.http import Http404
from django.http import JsonResponse
from neighbormade.utils.twilio import send_confirmation_code
from django.views.decorators.csrf import csrf_exempt
from neighbormade.models import Member, NeighbormadeToken, MemberStore, Upload
from neighbormade.models import StoreProduct


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
            neighbormade_token = NeighbormadeToken()
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
        neighbormade_token = NeighbormadeToken.objects.filter(
            token=token).first()
        if neighbormade_token:
            return neighbormade_token.member


@csrf_exempt
def manage_store(request):
    member = get_member_from_headers(request.headers)
    if not member:
        return JsonResponse({'message': 'invalid_code'})

    if request.POST:
        member_store = MemberStore()
        member_store.member = member
        member_store.description = request.POST.get("description", "")
        member_store.status = request.POST.get("status", "")
        member_store.location = request.POST.get("location", "")

        if request.FILES:
            upload = Upload(file=request.FILES['file'])
            upload.save()
            image_url = upload.file.url
            member_store.business_photo = image_url

        member_store.save()

        return JsonResponse({
            'message': 'success',
            'store_id': member_store.id
        })
    if request.method == 'GET':
        member_stores = MemberStore.objects.filter(member=member).values()
        return JsonResponse(list(member_stores), safe=False)

    return JsonResponse({'message': 'invalid_code'})


@csrf_exempt
def manage_product(request):
    member = get_member_from_headers(request.headers)
    if not member:
        return JsonResponse({'message': 'invalid_code'})

    if request.POST:
        store_id = int(request.POST.get("store_id", 0))
        # fetch store_id:
        member_store = MemberStore.objects.filter(
            member=member, id=store_id).first()

        if not member_store:
            return JsonResponse({'message': 'store_not_found'})

        # create product
        store_product = StoreProduct()
        store_product.member = member
        store_product.memberstore = member_store
        store_product.description = request.POST.get("description", "")
        store_product.price = float(request.POST.get("price", 0.0))

        if request.FILES:
            upload = Upload(file=request.FILES['photo1'])
            upload.save()
            image_url = upload.file.url
            store_product.photo1 = image_url

        store_product.save()
        print("EHRERE")
        return JsonResponse({
            'message': 'success',
            'store_id': store_product.id
        })
    if request.method == 'GET':
        store_products = StoreProduct.objects.filter(
            member=member).values()
        return JsonResponse(list(store_products), safe=False)

    return JsonResponse({'message': 'invalid_code'})


@csrf_exempt
def test_login(request):
    return render(request, 'test/login.html')


@csrf_exempt
def test_store(request):
    return render(request, 'test/store.html')


@csrf_exempt
def test_product(request):
    return render(request, 'test/product.html')
