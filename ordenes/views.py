from django.shortcuts import render
from .models import ItemOrden
from .formulario import FormCreacionOrden
from carrito.carrito import Carrito
import stripe
from django.http import JsonResponse
import os

STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY')
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY')

def crear_orden(request):
    carrito = Carrito(request)
    if request.method == 'POST':
        formulario = FormCreacionOrden(request.POST)
        if formulario.is_valid():
            orden = formulario.save()
            for item in carrito:
                ItemOrden.objects.create(orden=orden, producto=item['producto'],
                                         precio=item['precio'],
                                         cantidad=item['cantidad'])
            # Limpiar el carrito
            precio = carrito.obtener_precio_total
            carrito.limpiar_carrito()
            return render(request,
                          'pagos/stripe.html',
                          {'orden': orden, 
                           'precio': precio,
                           'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY})
    else:
        formulario = FormCreacionOrden()
    return render(request, 
                  'ordenes/crear.html', 
                  {'carrito': carrito, 'formulario': formulario})

def SesionPagoStripe(request, precio):
    YOUR_DOMAIN = "http://127.0.0.1:8000/"
    stripe.api_key = STRIPE_SECRET_KEY
    precio = int(float(precio))*100
    checkout_session = stripe.checkout.Session.create(
            line_items=[
                {
                    'price_data': {
                        'currency': 'mxn',
                        'unit_amount': precio,
                        'product_data': {
                            'name': 'Tu pedido',
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + 'ordenes/success/',
            cancel_url=YOUR_DOMAIN + 'ordenes/cancel/',
            )
    return JsonResponse(
        {
            'id': checkout_session.id
        }
    )

def pago_exitoso(request):
    return render(request, 'ordenes/creado.html')

def pago_cancelado(request):
    return render(request, 'ordenes/cancelado.html')
