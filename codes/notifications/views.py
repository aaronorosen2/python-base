from django.shortcuts import render

def notify(request):
    return render(request, "notification.html")

def notification(request):
    return render(request, "getnotification.html")
