from django.urls import path
from users.views import PaymentListAPIView
from users.apps import UsersConfig


app_name = UsersConfig.name


urlpatterns = [
            path('payment/', PaymentListAPIView.as_view(), name='payment-list')
              ]
