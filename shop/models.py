from djangoToy.custom import MyCustomModel
from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.

class Product(MyCustomModel):
    price = models.DecimalField(max_digits=8, decimal_places=2)
    name = models.CharField(max_length=255)
    img = models.TextField()
    description = models.TextField()


