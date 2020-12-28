from django.urls import path
from . import views

urlpatterns = [
    path('/Item', views.Item, name='Item'),
    path('/ItemDetail/<int:pk>', views.ItemDetail, name="ItemDetail"),
    path('/OrderItem/<int:pk>', views.OrderItem, name="OrderItem"),
    path('/Checkout', views.Checkout, name="Checkout"),
    path('/Subscribe', views.Subscribe, name="Subscribe"),
    path('/brainTreeSubscription', views.brainTreeSubscription,
         name="brainTreeSubscription"),
]
