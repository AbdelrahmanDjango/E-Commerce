import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from orders.models import Order
from .tasks import payment_completed

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status = 400)
    
    # if event.type == 'checkout.session.completed':
    #     session = event.data.object
    #     if session.mode == 'payment' and session.payment.status == 'paid':
    #         try:
    #             order = Order.objects.get(id = session.client_reference_id)
    #         except Order.DoesNotExist:
    #             return HttpResponse(status = 404)
    #         order.paid = True
    #         order.save()
    # return HttpResponse(status = 200)
    # if event.type == 'checkout.session.completed':
    #      session = event.data.object
    #      if session.mode == 'payment' and session.payment.status == 'paid':
    #         try:
    #            order = Order.objects.get(id=session.client_reference_id)
    #         except Order.DoesNotExist:
    #            return HttpResponse(status=404)
    #         order.paid = True
    #         order.save()
    # return HttpResponse(status=200)
    # ...

    if event.type == 'checkout.session.completed':

        # Information about this event : 'checkout.session.completed'
        session = event.data.object
        payment_intent_id = session.payment_intent
        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if payment_intent.status == 'succeeded':
                order = Order.objects.get(id=session.client_reference_id)
                order.paid = True
                order.stripe_id = session.payment_intent
                order.save()
                payment_completed.delay(order.id)
        except stripe.error.StripeError as e:
            # Handle Stripe errors, log them, etc.
            print(f"Error retrieving PaymentIntent: {e}")
        except Order.DoesNotExist:
            return HttpResponse(status=404)





