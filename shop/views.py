from django.shortcuts import render
from shop import models
from djangoToy.custom import MyListView, MyCreateView, MyDeleteView, MyUpdateView, MyDetailView
from django.urls import reverse_lazy

# Create your views here.


def index(request):
    return render(request, 'main/index.html')


class ProductListView(MyListView):
    model = models.Product
    template_name = 'main/products/product_list.html'


class ProductDetailView(MyDetailView):
    model = models.Product
    template_name = 'main/products/product_detail.html'

class ProductDeleteView(MyDeleteView):
    model = models.Product
    template_name = 'main/products/product_delete.html'
    success_url = reverse_lazy('prodotti')

class ProductCreateView(MyCreateView):
    fields = ['name','price','description','img']
    model = models.Product
    template_name = 'main/products/product_form.html'
    success_url = reverse_lazy('prodotti')