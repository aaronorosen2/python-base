from django.urls import path
from . import views

urlpatterns = [
    path('get/org',views.OrgApiView.as_view(),name='org-data'),
    path('get/org/<str:pk>',views.OrgApiView.as_view(),name='org-data_id'),

    path('get/channel',views.ChannelApiView.as_view(),name='channel-data'),
    path('get/channel/<str:pk>',views.ChannelApiView.as_view(),name='channel-data_id'),

    path('get/member',views.MemberApiView.as_view(),name='member-data'),
    path('get/member/<str:pk>',views.MemberApiView.as_view(),name='member-data_id'),

    path('get/channelmember',views.ChannelMemberApiView.as_view(),name='channel-member-data'),
    path('get/channelmember/<str:pk>',views.ChannelMemberApiView.as_view(),name='channel-member-data_id'),

    path('get/message/channel',views.MessageChannelApiView.as_view(),name='message_channel_data'),
    path('get/message/channel/<str:pk>',views.MessageChannelApiView.as_view(),name='message_channel_data_id'),
    
    path('get/message/user',views.MessageUserApiView.as_view(),name='message_user_data'),
    path('get/message/user/<str:pk>',views.MessageUserApiView.as_view(),name='message_user_data_id'),

    path('get/message/sms',views.MessageSMSApiView.as_view(),name='message_sms_data'),
    path('get/message/sms/<str:pk>',views.MessageSMSApiView.as_view(),name='message_sms_data_id'),

    # It will fetch perticular User records    
    path('get/user/paginatedmessages/' ,views.GetUserMessageApiView.as_view(),name='message_user_till'),
    # It will fetch perticular group records    
    path('get/channel/paginated_messages/' ,views.GetGroupMessageApiView.as_view(),name='message_user_till'),
    # It will fetch all user and Group 
    path('get/user_connected_list/', views.List_All_user.as_view(), name='list_user'),
]