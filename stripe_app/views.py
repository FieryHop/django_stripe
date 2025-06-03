import stripe
from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse, HttpResponse
from .models import Item, Order


def get_stripe_api_key(currency):
    return settings.STRIPE_KEYS[currency]['secret']


def item_detail(request, id):
    item = get_object_or_404(Item, id=id)
    stripe_public_key = settings.STRIPE_KEYS[item.currency]['public']

    return render(request, 'stripe_app/item.html', {
        'item': item,
        'stripe_public_key': stripe_public_key
    })


def buy_item(request, id):
    item = get_object_or_404(Item, id=id)
    stripe.api_key = get_stripe_api_key(item.currency)

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )

    return JsonResponse({'session_id': session.id})


def order_detail(request, id):
    order = get_object_or_404(Order, id=id)
    items = order.items.all()

    currency = items[0].currency if items else 'USD'
    stripe_public_key = settings.STRIPE_KEYS[currency]['public']

    return render(request, 'stripe_app/order.html', {
        'order': order,
        'items': items,
        'total_price': order.get_total_price(),
        'stripe_public_key': stripe_public_key
    })


def buy_order(request, id):
    order = get_object_or_404(Order, id=id)
    items = order.items.all()
    currency = items[0].currency if items else 'USD'
    stripe.api_key = get_stripe_api_key(currency)

    line_items = []
    for item in items:
        line_items.append({
            'price_data': {
                'currency': item.currency,
                'product_data': {
                    'name': item.name,
                },
                'unit_amount': int(item.price * 100),
            },
            'quantity': 1,
        })

    discounts = []
    if order.discount and order.discount.stripe_id:
        discounts.append({'coupon': order.discount.stripe_id})

    tax_rates = []
    if order.tax and order.tax.stripe_id:
        tax_rates = [order.tax.stripe_id]

    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        discounts=discounts,
        tax_id_collection={
            'enabled': bool(tax_rates),
        },
        mode='payment',
        success_url='https://example.com/success',
        cancel_url='https://example.com/cancel',
    )

    return JsonResponse({'session_id': session.id})

def home(request):
    return HttpResponse("Welcome to the Store! Visit /item/1/ or /order/1/")
# Create your views here.
