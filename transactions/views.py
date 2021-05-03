from django.shortcuts import render
from transactions.models import Transazioni
from django.db.models import Avg
# Create your views here.

def index(request):
    context = {}
    context["transazioni"] = stat = Transazioni.objects.all().aggregate(Avg('importo'))
    return render(request, "main/index.html", context)