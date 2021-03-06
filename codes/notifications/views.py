from django.shortcuts import render

def notify(request):
    return render(request, "notification.html")

def notification(request):
    return render(request, "getnotification.html")

def admin_monitoring(request):
    return render(request, "notification-queue.html")

def vstream_html(request):
    return render(request, "vstream.html")