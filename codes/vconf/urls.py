from .views import UploadCategory
from django.urls import path
from .views import UploadRoomLogo, EditRoomLogo, RoomInfoView, \
                   RoomVisitor, RecordingUpload, BrandInfo, ChannelList

urlpatterns = [
    path('room_info/', RoomInfoView.as_view(), name='room_info'),
    path('brand_info/<str:pk>', BrandInfo.as_view(), name='brand_info'),
    path('channel_list/', ChannelList.as_view(), name='channel_list'),
    path('upload/record_video/', RecordingUpload.as_view(), name='recording_upload'),
    path('upload/room_logo/', UploadRoomLogo.as_view(), name='logo_upload'),
    path('edit/room_logo/', EditRoomLogo.as_view(), name='edit_room_logo'),
    path('room_visitor/', RoomVisitor.as_view(), name='room_visitor'),
    path('category/', UploadCategory.as_view(), name='category'),
]
