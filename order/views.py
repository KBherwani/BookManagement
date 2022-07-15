import json
from datetime import *

import stripe
from django.utils import timezone
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from BookManagement import settings
from Books.models import Book
from order.models import Cart, CartItem, Order, OrderItem


class Addtocart(View):
    model = Cart

    def get(self, request, *args, **kwargs):
        book_obj = get_object_or_404(Book, id=kwargs.get('pk'))
        quantity = 1
        context = {}
        context["data"] = book_obj
        cart, cart_created = Cart.objects.get_or_create(
            user=self.request.user,
            defaults={'total': book_obj.price * quantity}
        )

        item, created = CartItem.objects.get_or_create(
            cart=cart,
            book=book_obj,
            defaults={'quantity': quantity, 'price': book_obj.price, }
        )
        cart = item.cart
        cart.update_total()
        self.request.session['cart_quantity'] = CartItem.objects.filter(
            cart=cart).count()
        cart_obj = reverse('order:clear_cart', args={cart.pk})
        return JsonResponse(
            {"status": "success", "cart_obj": cart_obj,
             "items_count": CartItem.objects.filter(cart=cart).count()
             })


class Clear_cart(View):
    model = Cart
    template_name = 'DetailView.html'

    def get(self, request, *args, **kwargs):
        context = {}
        cart_obj = get_object_or_404(Cart, id=kwargs.get('pk'))
        cart_obj.delete()
        self.request.session.modified = True
        del self.request.session['cart_quantity']
        return HttpResponse("Cart Cleared!")


class CartView(View):
    template_name = "cart_view.html"
    # from django.shortcuts import get_object_or_404

    def get(self, *args, **kwargs):
        cart_obj = get_object_or_404(Cart, user=self.request.user)

        cart_item_obj = CartItem.objects.filter(cart=cart_obj)
        context = {'cart': cart_item_obj, 'total': cart_obj.total,
                   'items_count': cart_item_obj.count(),
                   }
        return render(self.request, self.template_name, context=context)


class Cart_update(View):
    def post(self, *args, **kwargs):
        if self.request.META.get('HTTP_X_REQUESTED_WITH') == \
                'XMLHttpRequest' and self.request.method == "POST":
            cart_item_obj, created = CartItem.objects.get_or_create(
                pk=self.request.POST.get('pk'))
            cart_item_obj.quantity = int(self.request.POST.get("quantity"))
            price = int(
                self.request.POST.get("quantity")) * cart_item_obj.book.price
            cart_item_obj.price = price
            cart_item_obj.save()
            cart = cart_item_obj.cart
            cart.update_total()
            self.request.session['cart_quantity'] = \
                CartItem.objects.filter(cart=cart).count()
            return JsonResponse(
                {"status": "success", "pk": self.request.POST.get('pk'),
                 "price": price, 'total': cart.total,
                 "items_count": CartItem.objects.filter(
                     cart=cart_item_obj.cart).count()
                 })


def delete_cart_item(request):
    if request.META.get('HTTP_X_REQUESTED_WITH') == \
            'XMLHttpRequest' and request.method == "POST":
        cart_item_obj = CartItem.objects.get(
            pk=request.POST.get('pk'))
        cart = cart_item_obj.cart
        cart_item_obj.delete()
        cart.update_total()
        request.session['cart_quantity'] = CartItem.objects.filter(
            cart=cart).count()

        return JsonResponse(
            {"status": "success", "pk": request.POST.get('pk'),
             'total': cart.total,
             'items_count': CartItem.objects.filter(cart=cart).count()

             })


class Checkout(View):
    template_name = 'checkout.html'
    model = Order

    def get(self, request, *args, **kwargs):
        cart = Cart.objects.get(user=self.request.user)
        cart_item_obj = CartItem.objects. \
            filter(cart=cart)
        order = Order.objects.create(
            user=self.request.user,
            order_at=timezone.now(),
            total=cart.total,
            order_id=Order.new_order_id()
        )
        OrderItem.objects.create(
            order=order,
            subtotal=cart.total
        )
        cart.delete()
        request.session['cart_quantity'] = CartItem.objects.filter(
            cart=cart).count()
        return render(request, self.template_name)


def online_payment(request):
    cart = Cart.objects.get(user=request.user)
    context = {'cart': cart}
    return render(request, 'payment_view.html', context=context)


@csrf_exempt
def payment_view(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        total = cart.total
        total = total * 100
        stripe.api_key = settings.SECRET_KEY
        if request.method == "POST":

            data = json.loads(request.body)
            # Create a PaymentIntent with the order amount and currency
            customer = stripe.Customer.create(
                name="Jenny",
                address={
                    "line1": "510 Townsend St",
                    "postal_code": "98140",
                    "city": "San Francisco",
                    "state": "CA",
                    "country": "US",
                },
            )
            intent = stripe.PaymentIntent.create(
                amount=total,
                customer=customer['id'],
                currency=data['currency'],
                metadata={'cart_id': Cart.objects.get(user=request.user).id},
                description="testing "
            )
            try:
                return JsonResponse({'publishableKey':
                                         settings.PUBLISHABLE_KEY, 'clientSecret': intent.client_secret})
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=403)


def paymentcomplete(request):
    if request.method == "POST":
        data = json.loads(request.POST.get("payload"))
        if data["status"] == "succeeded":
            return render(request, "payment-complete.html")


@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        customer_email = session["customer_details"]["email"]
        payment_intent = session["payment_intent"]
    if event['type'] == 'payment_intent.succeeded':
        cart = Cart.objects.get(pk=event['data']['object']['metadata']['cart_id'])
        order = Order.objects.create(
            user=cart.user,
            order_at=timezone.now(),
            total=cart.total,
            order_id=Order.new_order_id()
        )
        OrderItem.objects.create(
            order=order,
            subtotal=cart.total
        )
        cart.delete()
    return HttpResponse(status=200)
