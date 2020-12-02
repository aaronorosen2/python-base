from django.shortcuts import render

def notify(request):
    return render(request, "templates/notification.html")

def notification(request):
    return render(request, "templates/getnotification.html")
