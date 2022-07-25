from django.urls import path
from . import views

urlpatterns = [
    path('get/org',views.OrgApiView.as_view(),name='org-data'),
    path('get/channel',views.ChannelApiView.as_view(),name='channel-data'),
    path('get/message',views.MessageApiView.as_view(),name='message-data'),
    path('get/member',views.MemberApiView.as_view(),name='member-data'),
    path('get/channelmember',views.ChannelMemberApiView.as_view(),name='channel-member-data'),

    path('get/org/<str:pk>',views.OrgApiView.as_view(),name='org-data'),
    path('get/channel/<str:pk>',views.ChannelApiView.as_view(),name='channel-data'),
    path('get/message/<str:pk>',views.MessageApiView.as_view(),name='message-data'),
    path('get/member/<str:pk>',views.MemberApiView.as_view(),name='member-data'),
    path('get/channelmember/<str:pk>',views.ChannelMemberApiView.as_view(),name='channel-member-data'),

    # path('get/org/',views.orgapi,name='org-data'),


]