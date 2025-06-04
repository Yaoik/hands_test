from django.urls import path

from .views import CreatePaymentView

app_name = 'payment'

urlpatterns = [
    path('api/webhook/bank/', CreatePaymentView.as_view(), name='create-payment-webhook')
]
