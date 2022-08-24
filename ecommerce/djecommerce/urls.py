
from django.conf import settings
from django.conf.urls.static import  static
from django.urls import include, path
from . import views
from .views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name="djecommerce"

urlpatterns = [
    path('',HomeView.as_view(),name="home"),
    path("product/<slug>/",ItemDetailView.as_view(),name="product"),
    path("checkout",CheckoutView.as_view(),name="checkout"),
    path("add-to-cart/<slug>",views.add_to_cart,name="add_to_cart"),
    path("add-coupon/",AddCouponView.as_view(),name="add-coupon"),
    path("remove_from_cart/<slug>",views.remove_from_cart,name="remove_from_cart"),
    path("login",views.login_view,name="login_view"),
    path("logout",views.logout_view,name="logout_view"),
    path("signup",views.signup,name="signup"),
    path("order-summary/",OrderSummaryView.as_view(),name="order-summary"),
    path("remove_single_item_from_cart/<slug>",views.remove_single_item_from_cart,name="remove_single_item_from_cart"),
    path("payment/<payment_option>/",PaymentView.as_view(),name="payment"),
    path("request-refund/",RequestRefundView.as_view(),name="request-refund")
]

if  settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += staticfiles_urlpatterns()