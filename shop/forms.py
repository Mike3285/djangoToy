from django import forms
from . import models
# https://overiq.com/django-paypal-subscriptions-with-django-paypal/

subscription_options = [
    ('Basic', 'Basic (€9 EUR/Mese)'),
    ('Medium', 'Medium (€30 EUR/Mese)'),
    ('Full', 'Full (€50 EUR/Mese)'),
]


class ChoosePayForm(forms.Form):
    tipologia_account = forms.ChoiceField(required=True, help_text='Scegli',choices=subscription_options)