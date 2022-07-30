from django.urls import path
from . import views

urlpatterns = [
    path('get/org/',views.OrgApiView.as_view(),name='org-data'),
    # path('get/channel',views.channelapi,name='channel-data'),
    # path('get/org',views.orgapi,name='org-data'),


]