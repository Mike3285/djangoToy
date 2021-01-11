from django.shortcuts import render
from shop import models
from djangoToy.custom import MyListView, MyCreateView, MyDeleteView, MyUpdateView, MyDetailView
from django.urls import reverse_lazy
from shop import forms
# Create your views here.
from django.shortcuts import redirect

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


from django.urls import reverse
from django.shortcuts import render
from paypal.standard.forms import PayPalPaymentsForm


def process_payment(request):
    context = {}
    # What you want the button to do.
    subscription_plan = request.session.get('subscription_plan')
    context['subscription_plan'] = subscription_plan
    if subscription_plan == 'Basic':
        price = '9.00'
    if subscription_plan == 'Medium':
        price = '59.00'
    if subscription_plan == 'Full':
        price = '89.00'
    paypal_dict = {
        "cmd": "_xclick-subscriptions",
        "business": 'business@flowsy.io',
        "a3": price,  # monthly price
        "p3": 1,  # duration of each unit (depends on unit)
        "t3": "M",  # duration unit ("M for Month")
        "src": "1",  # make payments recur
        "sra": "1",  # reattempt payment on payment error
        "no_note": "1",  # remove extra notes (optional)
        "item_name": "mysubscription",

        "notify_url": request.build_absolute_uri(reverse('paypal-ipn')),
        "return": request.build_absolute_uri(reverse('return_view')),
        "cancel_return": request.build_absolute_uri(reverse('cancel_view')),
        "custom": "premium_plan",  # Custom command to correlate to some function later (optional)
    }
    # Create the instance.
    form = PayPalPaymentsForm(initial=paypal_dict)
    context['form'] = form

    return render(request, "payment.html", context)


def checkout(request):
    context = {}
    if request.method == 'POST':
        form = forms.ChoosePayForm(request.POST)
        if form.is_valid():
            request.session['subscription_plan'] = form.cleaned_data['tipologia_account']
            return redirect('process_payment')
    else:
        form = forms.ChoosePayForm()
        context['form'] = form
        return render(request, 'checkout.html', context)



def la_return_view(request):
    return render(request, 'return_view.html')
def la_cancel_view(request):
    return render(request, 'cancel_view.html')