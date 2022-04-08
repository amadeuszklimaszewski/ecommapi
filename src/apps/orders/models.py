from django.db import models
from django.contrib.auth import get_user_model

from src.apps.accounts.models import UserAddress, UserProfile
from src.apps.products.models import Product

User = get_user_model()


class Cart(models.Model):
    # id, create an order using current data and .cart_items for .order_items
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Cart {self.pk} of user {self.user.username}. Total: ${self.total}"

    @property
    def total(self):
        cartitems = self.cart_items.all()
        total = sum(item.final_price for item in cartitems)
        return total


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Item of cart #{self.cart.pk}. Quantity: {self.quantity}"

    @property
    def total_item_price(self) -> float:
        return self.quantity * self.product.price

    @property
    def total_discount_item_price(self) -> float:
        if self.product.discount_price:
            return self.quantity * self.product.discount_price
        else:
            return self.total_item_price

    @property
    def amount_saved(self) -> float:
        return round(self.total_item_price - self.total_discount_item_price, 2)

    @property
    def final_price(self) -> float:
        if self.product.discount_price:
            return self.total_discount_item_price
        return self.total_item_price


# ----------- # ----------- # ----------- # ----------- #


class Coupon(models.Model):
    code = models.CharField(max_length=50)
    amount = models.IntegerField()
    is_active = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.code} coupon for ${self.amount}"


# ----------- # ----------- # ----------- # ----------- #


# class PaymentDetails(models.Model):
#     stripe_charge_id = models.CharField(max_length=50)
#     user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True)
#     amount = models.FloatField()
#     created = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    address = models.ForeignKey(
        UserAddress, on_delete=models.SET_NULL, null=True, blank=True
    )
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    #  payment = models.ForeignKey(PaymentDetails, on_delete=models.SET_NULL)
    order_accepted = models.BooleanField(default=False)
    payment_accepted = models.BooleanField(default=False)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Order #{self.pk} by user {self.user.username}."

    @property
    def before_coupon(self):
        orderitems = self.order_items.all()
        total = sum(item.final_price for item in orderitems)
        if discount := self.coupon.amount:
            total = total - discount
        return total

    @property
    def total(self):
        total = self.before_coupon
        if discount := self.coupon.amount:
            total = total - discount
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Item of {self.order.pk} order. Quantity: {self.quantity}"

    @property
    def total_item_price(self) -> float:
        return self.quantity * self.product.price

    @property
    def total_discount_item_price(self) -> float:
        return self.quantity * self.product.discount_price

    @property
    def amount_saved(self) -> float:
        return self.total_item_price - self.total_discount_item_price

    @property
    def final_price(self) -> float:
        if self.product.discount_price:
            return self.total_discount_item_price
        return self.total_item_price
