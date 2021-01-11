"""djangoToy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from shop import views

urlpatterns = [
    path('', views.index, name='index'),
    path('products', views.ProductListView.as_view(), name='prodotti'),
    path('products/create', views.ProductCreateView.as_view(), name='prodottocreate'),
    path('products/<int:pk>', views.ProductDetailView.as_view(), name='prodottodetail'),
    path('products/del/<int:pk>', views.ProductDeleteView.as_view(), name='prodottodelete'),
    path('payment', views.process_payment, name='process_payment'),
    path('checkout', views.checkout, name='checkout'),
    path('return', views.la_return_view, name='return_view'),
    path('canceled', views.la_cancel_view, name='cancel_view'),

]
