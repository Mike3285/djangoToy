from paypal.standard.ipn.signals import valid_ipn_received
from django.dispatch import receiver
from paypal.standard.models import ST_PP_COMPLETED
from django.core.mail import EmailMessage
from django.conf import settings
from datetime import datetime
from django.shortcuts import get_object_or_404

@receiver(valid_ipn_received)
def ipn_receiver(sender, **kwargs):
    ipn_obj = sender

    # check for Buy Now IPN
    if ipn_obj.txn_type == 'web_accept':

        if ipn_obj.payment_status == ST_PP_COMPLETED:
            # payment was successful
            order = get_object_or_404(Item, id=ipn_obj.invoice)
            if order.get_total_cost() == ipn_obj.mc_gross:
                # mark the order as paid
                order.paid = True
                order.save()

    # check for subscription signup IPN
    elif ipn_obj.txn_type == "subscr_signup":
        # get user id and activate the account
        id = ipn_obj.custom
        user = settings.AUTH_USER_MODEL.objects.get(id=id)
        user.active = True
        user.save()

        subject = 'Sign Up Complete'

        message = 'Thanks for signing up!'

        email = EmailMessage(subject,
                             message,
                             'admin@myshop.com',
                             [user.email])

        email.send()

    # check for subscription payment IPN
    elif ipn_obj.txn_type == "subscr_payment":

        # get user id and extend the subscription
        id = ipn_obj.custom
        user = User.objects.get(id=id)
        # user.extend()  # extend the subscription

        subject = 'Your Invoice for {} is available'.format(
            datetime.strftime(datetime.now(), "%b %Y"))

        message = 'Thanks for using our service. The balance was automatically ' \
                  'charged to your credit card.'

        email = EmailMessage(subject,
                             message,
                             'admin@myshop.com',
                             [user.email])

        email.send()

    # check for failed subscription payment IPN
    elif ipn_obj.txn_type == "subscr_failed":
        pass

    # check for subscription cancellation IPN
    elif ipn_obj.txn_type == "subscr_cancel":
        pass



@receiver(valid_ipn_received)
def paypal_payment_received(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # WARNING !
        # Check that the receiver email is the same we previously
        # set on the `business` field. (The user could tamper with
        # that fields on the payment form before it goes to PayPal)
        if ipn_obj.receiver_email != 'your-paypal-business-address@example.com':
            # Not a valid payment
            return

        # ALSO: for the same reason, you need to check the amount
        # received, `custom` etc. are all what you expect or what
        # is allowed.
        try:
            my_pk = ipn_obj.invoice
            mytransaction = MyTransaction.objects.get(pk=my_pk)
            assert ipn_obj.mc_gross == mytransaction.amount and ipn_obj.mc_currency == 'EUR'
        except Exception:
            logger.exception('Paypal ipn_obj data not valid!')
        else:
            mytransaction.paid = True
            mytransaction.save()
    else:
        logger.debug('Paypal payment status not completed: %s' % ipn_obj.payment_status)