from django.shortcuts import render
import os,json
from rest_framework.views import APIView
from courses.models import Course
from rest_framework import status
from rest_framework.response import Response
import stripe
from payments.models import PaymentIntent,Payment
from decimal import Decimal
from users.models import User


# Create your views here.
stripe_api_key=os.environ.get("STRIPE_APIKEY")
endpoint_secret="whsec_..."

stripe.api_key=stripe_api_key

class PaymentHandler(APIView):
    def post(self,request):
        if request.body:
            body=json.loads(request.body)
            if body and len(body):
                course_line_items=[]
                cart_course=[]
                for item in body:
                    try:
                        course=Course.objects.get(course_uuid=item)
                        line_item={
                            "price_data":{
                                "currency":"usd",
                                "unit_amount":int(course.price*100),
                                "product_data":{
                                    "name":course.title,
                                },
                            },
                            "quantity":1,
                        }
                        course_line_items.append(line_item)
                        cart_course.append(course)
                    except Course.DoesNotExist:
                        return Response(status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        checkout_session=stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=course_line_items,
            mode="payment",
            success_url="http://localhost:3000/",
            cancel_url="http://localhost:3000/",
        )
        intent=PaymentIntent.objects.create(
            payment_intent_id=checkout_session.payment_intent,
            checkout_id=checkout_session.id,
            user=User.objects.get(id=1),
        )
        intent.course.add(*cart_course)
        return Response({"url":checkout_session.url})

class Webhook(APIView):
    def post(self,request):
        payload=request.body
        sig_header=request.META["HTTP_STRIPE_SIGNATURE"]

        event=None

        try:
            event=stripe.Webhook.construct_event(
                payload=payload,sig_header=sig_header,secret=endpoint_secret
            )
        except:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        if event['type']=="checkout.session.completed":
            session=event["data"]["object"]

            try:
                intent=PaymentIntent.objects.get(checkout_id=session.id,payment_intent_id=session.payment_intent)
            
            except PaymentIntent.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            Payment.objects.create(
                payment_intent=intent,
                total_amount=Decimal(session.amount_total)/100,
            )
            intent.user.paid_courses.add(*intent.course.all())

            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# no-3,len-1.35min
