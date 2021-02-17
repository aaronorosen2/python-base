from django.urls import path
from . import views

urlpatterns = [
    path('/Item', views.Item, name='Item'),
    path('/userItem', views.userItem, name='userItem'),
    path('/ItemDetail/<int:pk>', views.ItemDetail, name="ItemDetail"),
    path('/userItemDetail/<int:pk>', views.userItemDetail, name="userItemDetail"),
    path('/OrderItem/<int:pk>', views.OrderItem, name="OrderItem"),
    path('/Checkout', views.Checkout, name="Checkout"),
    path('/UserOrderItem/<int:pk>', views.UserOrderItem, name="UserOrderItem"),
    path('/UserCheckout', views.UserCheckout, name="UserCheckout"),
    path('/Subscribe', views.Subscribe, name="Subscribe"),
    path('/brainTreeSubscription', views.brainTreeSubscription,
            name="brainTreeSubscription"),
    path('/userSubscribe', views.userSubscribe, name="userSubscribe"),
    path('/userbrainTreeSubscription', views.userbrainTreeSubscription,
            name="userbrainTreeSubscription"),
    path('/userOrderList', views.userOrderList, name='userOrderList'),
    
]
