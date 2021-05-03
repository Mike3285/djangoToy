from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from djangoToy import custom
# Create your models here.



class Invoice(custom.MyCustomModel):
    account = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='invoices', on_delete=models.CASCADE, blank=True, null=True, verbose_name=_('proprietario'))
    paid = models.BooleanField(default=False,)
    paid_at = models.DateTimeField(editable=False,null=True, verbose_name=_('Creato'), help_text=_('Data e ora di creazione'))