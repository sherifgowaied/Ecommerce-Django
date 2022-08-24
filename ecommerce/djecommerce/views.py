from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView , DetailView , View
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.auth import login as auth_login
from .forms import ChekoutForm, CouponForm, RefundForm
from django.contrib.auth.decorators import login_required
import stripe
import random 
import string 


def create_ref_code():
    return "".join(random.choices(string.ascii_lowercase+string.digits , k=20))


# Create your views here.

class HomeView(ListView):
    model = Item
    template_name = "home.html"
    paginate_by =10

class ItemDetailView(DetailView):
    model=Item
    template_name="product.html"


def is_valid_form(values):
    valid =True
    for field in values:
        if field == '':
            valid=False
    return valid


class OrderSummaryView(LoginRequiredMixin ,View):
    def get(self  ,*args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user , ordered=False)
            context = {
                "object":order
            }
            return render(self.request,"order_summary.html",context)
        except ObjectDoesNotExist:
            messages.info(self.request,"You don't have active order")
            return redirect("djecommerce:home")
    
    

def home(request):
    context = {
        "items":Item.objects.all()
    }
    return render(request,"home.html",context)

def product(request):
    context={
        "items":Item.objects.all()
    }
    return render(request,"product.html")


class CheckoutView(View):
    def get(self , *args, **kwargs):
        #form
        try:
            order = Order.objects.get(user = self.request.user , ordered=False)
            form = ChekoutForm()
            context = {
                "form":form,
                "order":order,
                "couponform":CouponForm(),
                "DISPLAY_COUPON_FORM":True
            }
            # print("1")
            try:
                print("search for shipping address")
                shipping_address_qs = Address.objects.filter(
                        user = self.request.user , 
                        address_type = 'S',
                        default = True
                        ).all()[0]
            except:
                shipping_address_qs =None
            print("finshish search for shipping address")
            print("if search address exist")
            if shipping_address_qs:
                print(" start search for shipping address")
                context.update({"default_shipping_address":shipping_address_qs})
                
                # 
            # except:
            shipping_address_qs=None
            try:
                billing_address_qs = Address.objects.filter(
                    user = self.request.user , 
                    address_type = 'B',
                    default = True
                    )[0]
                # print("1")
                if billing_address_qs:
                    context.update({"default_billing_address":billing_address_qs})
                    # print("1")
            except:
                billing_address_qs=None
            return render(self.request,"checkout.html",context)
        except ObjectDoesNotExist :
            messages.info(self.request,"you do not have an active order")
            return redirect("djecommerce:order-summary")

    def post(self,*args, **kwargs):
        form = ChekoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user , ordered=False)
            if form.is_valid():
            
                use_default_shipping = form.cleaned_data.get("use_default_shipping")
                if use_default_shipping:
                    # print("Using default shipping adress")
                    address_qs = Address.objects.filter(
                    user = self.request.user , 
                    address_type = 'S',
                    default = True
                    )
                    if address_qs:
                        shipping_address = address_qs[0]
                        order.shipping_address = shipping_address
                        order.save()
                    else:
                        messages.info(self.request,"No default shipping address available")
                        return redirect("djecommerce:checkout")
                else:
                
                    shipping_address1 = form.cleaned_data.get("shipping_address")
                    shipping_address2=form.cleaned_data.get("shipping_address2")
                    shipping_country = form.cleaned_data.get("shipping_country")
                    shipping_zip = form.cleaned_data.get("shipping_zip")
                    
                    if is_valid_form([shipping_address1,shipping_country,shipping_zip]):

                        shipping_address =Address(
                            user = self.request.user,
                            street_address = shipping_address1,
                            apartment_address = shipping_address2,
                            country = shipping_country,
                            zip = shipping_zip,
                            address_type = "S"
                        )
                        print(form.cleaned_data)
                        print("this form is valid")
                        shipping_address.save()
                        order.shipping_address = shipping_address
                        order.save()
                        set_default_shipping = form.cleaned_data.get("set_default_shipping")
                        if set_default_shipping:
                            shipping_address.default = True
                            shipping_address.save()

                    else:
                        messages.info(self.request,"Please fill in the required shipping address fields")
                        return redirect("djecommerce:checkout")

                use_default_billing = form.cleaned_data.get("use_default_billing")
                same_billing_address = form.cleaned_data.get("same_billing_address")
                
                if same_billing_address:
                    billing_address = shipping_address
                    billing_address.pk = None
                    billing_address.save()
                    billing_address.address_type = "B"
                    billing_address.save()
                    order.billing_address = billing_address
                    order.save()

                elif use_default_billing:
                    # print("Using default shipping adress")
                    address_qs = Address.objects.filter(
                    user = self.request.user , 
                    address_type = 'B',
                    default = True
                    )
                    if address_qs:
                        billing_address = address_qs[0]
                        order.billing_address = billing_address
                        order.save()
                    else:
                        messages.info(self.request,"No default billing address available")
                        return redirect("djecommerce:checkout")
                else:
                    # print("User is entering new billing address")
                    billing_address1 = form.cleaned_data.get("billing_address")
                    billing_address2=form.cleaned_data.get("billing_address2")
                    billing_country = form.cleaned_data.get("billing_country")
                    billing_zip = form.cleaned_data.get("billing_zip")
                    
                    if is_valid_form([billing_address1,billing_country,billing_zip]):

                        billing_address =Address(
                            user = self.request.user,
                            street_address = billing_address1,
                            apartment_address = billing_address2,
                            country = billing_country,
                            zip = billing_zip,
                            address_type = "B"
                        )
                        # print(form.cleaned_data)
                        # print("this form is valid")
                        billing_address.save()
                        order.billing_address = billing_address
                        order.save()
                        set_default_billing = form.cleaned_data.get("set_default_billing")
                        if set_default_billing:
                            billing_address.default = True
                            billing_address.save()

                    else:
                        messages.info(self.request,"Please fill in the required Billing  address fields")
                        return redirect("djecommerce:checkout")
                    
                    

                payment_option = form.cleaned_data.get("payment_option")
                # TODO: add redirect to the selected payment option
                if payment_option =="S":
                    return redirect("djecommerce:payment",payment_option="stripe")
                elif payment_option =="P":
                    return redirect("djecommerce:payment",payment_option="paypal")
                else:
                    messages.info(self.request,"Inavalid payment option")
                    return redirect("djecommerce:checkout")

        except ObjectDoesNotExist:
            messages.info(self.request,"You don't have active order")
            return redirect("djecommerce:checkout")

class PaymentView(View):
    
    def get(self,*args, **kwargs):
        ## the order
        order = Order.objects.get(user = self.request.user , ordered =False)
        if order.billing_address:
            context = {
                "order":order,
                "DISPLAY_COUPON_FORM":False ,
                "STRIPE_PUBLIC_KEY":"pk_test_TYooMQauvdEDq54NiTphI7jx"
            }
            return render(self.request,"payment.html",context)
        else: 
            messages.info(self.request,"You don't have billing adress")
            return redirect("djecommerce:checkout")

    
    def post(self,*args, **kwargs):
        order = Order.objects.get(user = self.request.user , ordered =False)
        token = self.request.POST.get("stripeToken")
        ## `source` is obtained with Stripe.js; see https://stripe.com/docs/payments/accept-a-payment-charges#web-create-token
        amount = order.get_total_price() * 100
        stripe.api_key = settings.STRIPE_SECERT_KEY

        try:
        # Use Stripe's library to make requests...
            charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,
            description="My First Test Charge (created for API docs)",
            )

            #create payment
            payment = Payment()
            payment.stripe_charge_id = charge["id"]
            payment.user = self.request.user
            payment.amount = amount
            payment.save()

            #assign the payment to the order 
            order_items = order.items.all()
            order_items.update(ordered=True)
            for item in order_items:
                item.save()

            order.ordered =True
            # TODO  assin ref code 
            order.ref_code = create_ref_code()
            order.payment = payment 
            order.save()

            messages.success(self.request ,"Your order was successful !")
            return redirect("djecommerce:home")

        except stripe.error.CardError as e:
        # Since it's a decline, stripe.error.CardError will be caught

            print('Status is: %s' % e.http_status)
            print('Code is: %s' % e.code)
            # param is '' in this case
            print('Param is: %s' % e.param)
            print('Message is: %s' % e.user_message)
            messages.info(self.request ,f"{e.user_message}")
            return redirect("/djecommerce")

        except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
            messages.info(self.request ,"Rate limit error")
            return redirect("/djecommerce")

        except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe's API
            messages.info(self.request ,"Invalid parameters")
            return redirect("/djecommerce")

        except stripe.error.AuthenticationError as e:
        # Authentication with Stripe's API failed
        # (maybe you changed API keys recently)
            messages.info(self.request ,f"Not authenitacated")
            return redirect("/djecommerce")

        except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
            messages.info(self.request ,"Network error")
            return redirect("/djecommerce")

        except stripe.error.StripeError as e:
        # Display a very generic error to the user, and maybe send
        # yourself an email
            messages.info(self.request ,"Something went wrong. you are not charged , Please try again ")
            return redirect("/djecommerce")

        except Exception as e:
        # Something else happened, completely unrelated to Stripe
        # send email to our selfes
            messages.info(self.request ,"A serious error occured.  we have been notfied")

            return redirect("/djecommercedanger")
        
         
        

        
@login_required(login_url='/djecommerce/login')
def add_to_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_item , created = OrderItem.objects.get_or_create(item=item ,user=request.user,ordered=False)                                      
    order_qs = Order.objects.filter(user=request.user , ordered=False)
    if order_qs.exists():
        order = order_qs[0]
        #check if the  order item is  in order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity +=1
            order_item.save()
            messages.info(request,"this item quntity was updated")
            return HttpResponseRedirect(reverse("djecommerce:order-summary"))
        else:
            order.items.add(order_item)
            messages.info(request,"this item is added to your cart")
            return HttpResponseRedirect(reverse("djecommerce:order-summary"))
    else:
        order_date=timezone.now()
        order=Order.objects.create(user=request.user ,ordered_date=order_date)
        order.items.add(order_item)
        messages.info(request,"this item is added to your cart")
        return HttpResponseRedirect(reverse("djecommerce:order-summary"))

@login_required(login_url='/djecommerce/login')
def remove_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            order.items.remove(order_item)
            messages.info(request,"this item is removed to your cart")
            return HttpResponseRedirect(reverse("djecommerce:order-summary"))
        else:
            #add message saying the oreder doesn't contain the item
            messages.info(request,"this item is not in your cart")
            return HttpResponseRedirect(reverse("djecommerce:product", args=(slug,)))
    else:
        #add message saying the oreder doesn't contain the item
        messages.info(request,"You don't have a active order")
        return HttpResponseRedirect(reverse("djecommerce:product", args=(slug,)))


def login_view(request):
    if request.method == "POST":
    
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request,f"Logged in Successfully as {username} ")
            return HttpResponseRedirect(reverse("djecommerce:home"))
        else:
            messages.info(request,"Not valid username/password")
            return render(request, "login.html")
    else:
        return render(request,"login.html")

    



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("djecommerce:home"))
    


def signup(request):
    if request.method == "POST":
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        username= str(request.POST["username"])
        email = request.POST["email"]
        

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.info(request,"Passwords must match.")
            return render(request, "signup.html")

        # Attempt to create new user
        
        try:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name, email=email, password=password )
            user.save()
        except IntegrityError:
            messages.info(request,"Username already taken.")
            return render(request, "signun.html")
        login(request, user)
        messages.success(request,"Account Signed up Successfully")
        return HttpResponseRedirect(reverse("djecommerce:home"))
    else:
        return render(request,"signup.html")
    

@login_required(login_url='/djecommerce/login')
def remove_single_item_from_cart(request,slug):
    item = get_object_or_404(Item,slug=slug)
    order_qs = Order.objects.filter(user=request.user,ordered=False)
    if order_qs.exists():
        order=order_qs[0]
        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(
                item=item,
                user=request.user,
                ordered=False)[0]
            if order_item.quantity > 1 :
                order_item.quantity -=1
                order_item.save()
            else:
                order.items.remove(order_item)
            # order.items.remove(order_item)
            messages.success(request,"this item is quaninty is updated")
            return HttpResponseRedirect(reverse("djecommerce:order-summary"))
        else:
            #add message saying the oreder doesn't contain the item
            messages.info(request,"this item is not in your cart")
            return HttpResponseRedirect(reverse("djecommerce:order-summary"))
    else:
        #add message saying the oreder doesn't contain the item
        messages.info(request,"You don't have a active order")
        return HttpResponseRedirect(reverse("djecommerce:order-summary"))


def get_coupon(request,code):
    try:
        coupon = Coupon.objects.get(code = code)
        return coupon

    except ObjectDoesNotExist:
        messages.info(request,"This coupon doesn't exsist")
        return HttpResponseRedirect(reverse("djecommerce:checkout"))


class AddCouponView(View):
    def post(self,*args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get("code")
                order =Order.objects.get(user=self.request.user , ordered=False)
                order.coupon = get_coupon(self.request,code)
                order.save()
                messages.success(self.request,"Successfully added the coupon")
                return HttpResponseRedirect(reverse("djecommerce:checkout"))

            except ObjectDoesNotExist :
                messages.info(self.request,"You don't have a active order")
                return HttpResponseRedirect(reverse("djecommerce:checkout"))
                
    # TODO raise error
class RequestRefundView(View):
    def get(self,*args, **kwargs):
        form = RefundForm()
        context = {
            "form":form
        }
        return render(self.request,"request_refund.html",context)

    def post(self,*args, **kwargs):
        form = RefundForm(self.request.POST)
        if form.is_valid():
            ref_code = form.cleaned_data.get("ref_code") 
            message  = form.cleaned_data.get("message")
            email  = form.cleaned_data.get("email")
            # edit the order
            try:
                order = Order.objects.get(ref_code=ref_code)
                if order.ordered != True:
                    messages.info(self.request,"This order doesn't exist")
                    return redirect("djecommerce:request-refund")
                order.refund_requested =True
                order.save()
                
                # store the refund
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()


                
                
                messages.success(self.request,"Your request was received")
                return redirect("djecommerce:request-refund")

            except ObjectDoesNotExist :
                messages.info(self.request,"This order doesn't exist")
                return redirect("djecommerce:request-refund")

    
   