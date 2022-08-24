from re import A
from sqlite3 import Timestamp
from statistics import mode
from tabnanny import verbose
from django.urls import reverse
from secrets import choice
from django.db import models
from django.contrib.auth.models import AbstractUser
from .forms import COUNTRIES
CATEGORY_CHOICES =(
    ('S','Shirt'),
    ('SW','Sport wear'),
    ('OW','Out Wear')
)

LABEL_CHOICES =(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
)

ADDRESS_CHOICES =(
    ('B','Billing'),
    ('S','Shipping')
)




# Create your models here.
class User(AbstractUser):
    pass


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True , null=True)
    category = models.CharField(max_length=2,choices=CATEGORY_CHOICES)
    label = models.CharField(max_length=1,choices=LABEL_CHOICES )
    slug = models.SlugField()
    image = models.ImageField(upload_to="images",blank=True,null=True)
    description = models.TextField()
    

    def get_image(self):
        
        media ="/Users/mohamed/Desktop/django-ecommerce1/django-ecommerce-real/ecommerce/media"
        return  media + "/" + f"{self.image}" 
    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("djecommerce:product",kwargs={
            "slug":self.slug
        })
    
    def get_add_to_cart(self):
        return  reverse("djecommerce:add_to_cart",kwargs={
            "slug":self.slug
        })
    
    def remove_from_cart(self):
        return reverse("djecommerce:remove_from_cart",kwargs={
            "slug":self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orderitems")
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name="orderitem")
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.title}"

    def get_total_item_price(self):
        return self.quantity * self.item.price

    def get_total_discount_item_price(self):
        
        return self.quantity * self.item.discount_price

    def  get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_item_price()


    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_discount_item_price()
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="order" )
    ref_code = models.CharField(max_length=20,blank=True ,null=True )
    ordered = models.BooleanField(default=False)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    billing_address = models.ForeignKey("Address",related_name="billing_adress",on_delete=models.SET_NULL ,
        blank=True ,null=True)
    shipping_address = models.ForeignKey("Address",related_name="shipping_adress",on_delete=models.SET_NULL ,
        blank=True ,null=True)
    payment = models.ForeignKey("Payment",on_delete=models.SET_NULL ,
        blank=True ,null=True)
    coupon = models.ForeignKey("Coupon" ,on_delete=models.SET_NULL ,
        blank=True ,null=True)
    being_delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)


    """
    1.item added to cart
    2.add billing adress
    (Failed checkout)
    3.payment
    4. being develired
    5.Recevied
    6.refunds

    """


    def __str__(self):
        return f"{self.user.username}"

    def get_total_price(self):
        total = 0 
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total  -= self.coupon.amount
        return total 


class Address(models.Model):
    user = models.ForeignKey(User ,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = models.CharField(max_length=2, choices=COUNTRIES)
    zip = models.CharField(max_length=100)
    address_type = models.CharField(max_length=1,choices=ADDRESS_CHOICES)
    default = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username}:{self.street_address}"
    class Meta:
        verbose_name_plural = "Adresses"

class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=50)
    user = models.ForeignKey(User , on_delete=models.SET_NULL , blank=True , null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) :
        return f"{self.user.username}"


class Coupon(models.Model):
    code = models.CharField(max_length=15)
    amount = models.FloatField()


    def __str__(self):
        return f"{self.code}"


class Refund(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    reason = models.TextField()
    accepted = models.BooleanField(default=False)
    email = models.EmailField()

    def __str__(self):
        return f"{self.id} {self.reason}"