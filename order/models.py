from django.contrib.auth.models import User
from django.db import models
from django.db.models import Sum
import re
from Books.models import Book
from django.db.models import Max

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='user_cart')
    total = models.PositiveIntegerField()

    #
    # def cart_exits(self):
    #     return

    def update_total(self):
        cartitem = CartItem.objects.filter(cart__user=self.user)
        if len(cartitem) == 0:
            self.total = 0
            self.save()
        else:
            total = CartItem.objects.filter(cart__user=self.user).aggregate(
                total=Sum('price'))['total']
            self.total = total
            self.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()


class Address(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    line1 = models.CharField(max_length=150)
    line2 = models.CharField(max_length=150)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip = models.CharField(max_length=10)
    contact = models.CharField(max_length=12)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = (
        ('Success', 'Success'),
        ('Failed', 'Failed'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_at = models.DateTimeField()
    order_id = models.CharField(max_length=12)
    total = models.PositiveIntegerField()
    status = models.CharField(max_length=7, choices=STATUS_CHOICES,
                              null=True, blank=True)

    @classmethod
    def new_order_id(cls):
        try:
            order_id = cls.objects.latest('order_id').order_id
        except Exception as e:
            print(str(e))
            order_id = "ORD" + "0000"
        return re.sub('(\d+)', lambda x: str(int(x.group(0)) + 1).zfill(8), order_id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    subtotal = models.PositiveIntegerField()
