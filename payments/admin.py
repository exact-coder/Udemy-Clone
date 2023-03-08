from django.contrib import admin
from payments.models import Payment,PaymentIntent

# Register your models here.
class PaymentIntentAdmin(admin.ModelAdmin):
    list_display=['payment_intent_id','checkout_id','created']
    list_display_links=['payment_intent_id','checkout_id']
admin.site.register(PaymentIntent,PaymentIntentAdmin)

class PaymentAdmin(admin.ModelAdmin):
    list_display=['id','total_amount','created']
    list_display_links=['id','total_amount']
admin.site.register(Payment,PaymentAdmin)