from django.urls import path
from . import views

urlpatterns = [
    path('connect/', views.StripeConnectOnboardingView.as_view(), name='connect'),
    path('onboarding_complete/', views.CompleteOnboardingView.as_view(), name='onboarding_complete'),
    path('check_connection/', views.check_connection, name='check_connection'),
    path('checkout/', views.checkout, name='checkout'),
    path('payments/<int:lesson_id>/', views.payments_by_lesson, name='payments'),
]
