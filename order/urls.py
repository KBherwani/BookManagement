from django.urls import path
from order.views import *

app_name = "order"

urlpatterns = [
    path("cart/<int:pk>/", Addtocart.as_view(), name="cart"),
    path("clear_cart/<int:pk>/", Clear_cart.as_view(), name="clear_cart"),
    path("cart/", CartView.as_view(), name="cart"),
    path("cart_update/", Cart_update.as_view(), name="cart_update"),
    path("delete_item/", delete_cart_item, name="delete_cart_item"),
    path("checkout", Checkout.as_view(), name="checkout"),
    path('create-payment-intent', payment_view, name='payment'),
    path('payment-complete', paymentcomplete, name='paymentcomplete'),
    path('online-payment', online_payment, name='online-payment'),
    path('webhook', webhook, name='webhook'),





]
