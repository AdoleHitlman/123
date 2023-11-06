import stripe

from config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment_intent(amount, currency):
    intent = stripe.PaymentIntent.create(
        amount=amount,
        currency=currency
    )
    return intent


def retrieve_payment_intent(payment_id):
    intent = stripe.PaymentIntent.retrieve(payment_id)
    return intent
