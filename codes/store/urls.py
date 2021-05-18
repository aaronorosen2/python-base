from django.urls import path
from . import views

urlpatterns = [
        path('Item', views.Item, name='Item'),
        path('userItem', views.userItem, name='userItem'),
        path('ItemDetail/<int:pk>', views.ItemDetail, name="ItemDetail"),
        path('userItemDetail/<int:pk>', views.userItemDetail, name="userItemDetail"),
        path('OrderItem/<int:pk>', views.OrderItem, name="OrderItem"),
        path('Checkout', views.Checkout, name="Checkout"),
        path('UserOrderItem/<int:pk>', views.UserOrderItem, name="UserOrderItem"),
        path('UserCheckout', views.UserCheckout, name="UserCheckout"),
        path('Subscribe', views.Subscribe, name="Subscribe"),
        path('brainTreeSubscription', views.brainTreeSubscription,
                name="brainTreeSubscription"),
        path('userSubscribe', views.userSubscribe, name="userSubscribe"),
        path('userbrainTreeSubscription', views.userbrainTreeSubscription,
                name="userbrainTreeSubscription"),
        path('userbrainTreeUnsubscription', views.userbrainTreeUnsubscription,
                name="userbrainTreeUnsubscription"),
        path('subscriptionStatus', views.subscriptionStatus,
                name="subscriptionStatus"),
        path('userOrderList', views.userOrderList, name='userOrderList'),
        path('deleteImage', views.deleteImage, name='deleteImage'),
        path('userProfile', views.userProfile, name='userProfile'),
        path('TeacherUIBraintreeConfig', views.TeacherUIBraintreeConfig, name='TeacherUIBraintreeConfig'),
        path('TeacherUIItemsNeighbourhood', views.TeacherUIItemsNeighbourhood, name='TeacherUIItemsNeighbourhood'),
        
        # stripe
        path('stripePage', views.stripePage, name='stripePage'),
        path('stripeCharge', views.stripeCharge, name='stripeCharge'),
        path('StripeCheckout', views.StripeCheckout, name='StripeCheckout'),
        path("completeStripeSubscription", views.completeStripeSubscription, name="completeStripeSubscription"), #add
        path('Stripethank', views.Stripethank, name='Stripethank'),
        path('StripeConfiguration', views.StripeConfiguration, name='StripeConfiguration'),
        # FCM
        path('FCMDeviceTest', views.FCMDeviceTest, name='FCMDeviceTest'),
        path('StoreFCMToken', views.StoreFCMToken, name='StoreFCMToken'),
        # count member in neighborhood and items 
        path('ItemsAndMember', views.ItemsAndMember, name='ItemsAndMember'),
        path('profilePic', views.profilePic, name='profilePic'),
        # messages
        path('sendMessage', views.sendMessage, name='sendMessage'),
        path('getMessages', views.getMessages, name='getMessages'),
        path('getAllMessages', views.getAllMessages, name='getAllMessages'),
]
