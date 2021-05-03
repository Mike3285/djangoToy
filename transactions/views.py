from django.shortcuts import render
from transactions.models import Transazioni
# Create your views here.

def index(request):
    context = {}
    context["transazioni"] = Transazioni.objects.all()
    return render(request, "main/index.html", context)