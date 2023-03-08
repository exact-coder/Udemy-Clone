from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import User
from courses.models import Course

# Create your models here.

class PaymentIntent(models.Model):
    payment_intent_id=models.CharField(_("Payment Intent ID"), max_length=250)
    checkout_id=models.CharField(_("Checkout Id"), max_length=250)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    course=models.ManyToManyField(Course, verbose_name=_("Courses"))
    created=models.DateTimeField(_("Created"), auto_now=True, auto_now_add=False) 


class Payment(models.Model):
    payment_intent=models.ForeignKey(PaymentIntent, on_delete=models.CASCADE)
    total_amount=models.DecimalField(_("Total Amount"), max_digits=9, decimal_places=2)
    created=models.DateTimeField(_("Created"), auto_now=True, auto_now_add=False)