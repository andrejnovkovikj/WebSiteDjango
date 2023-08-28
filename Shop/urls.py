"""
URL configuration for Shop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import views
from django.contrib import admin
from django.urls import include, path
from myapp.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home, name="home"),
    path('home/',home, name="home"),
    path('shop/',shop, name="shop"),
    path('shop/men/',shop_men, name="shop_men"),
    path('shop/women/',shop_women, name="shop_men"),
    path('shop/<str:sex_name>/<str:type_name>/',products, name='products'),
    path('random/',random, name="random"),
    path('register/',registerPage, name="register"),
    path('login/',loginPage, name="login"),
    path('logout/',logoutUser,name="logoutUser"),
    path('product/<int:code>/', singleProduct, name='singleProduct'),
    path('shoppingCart/', shoppingCart,name='shoppingCart'),
    path('add_to_cart/<int:product_code>/',add_to_cart,name='add_to_cart'),
    path('remove_from_cart/<int:item_id>/', remove_from_cart,name='remove_from_cart'),
    path('checkout/',checkout,name='checkout'),
    path('payment/',payment, name='payment'),
    path('successfulPayment/',successfulPayment,name='success')
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
