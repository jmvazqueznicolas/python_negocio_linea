from django.shortcuts import render
from django.contrib import messages
from .mailchimp import add_subscriber
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')

def suscripcion(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            add_subscriber(email)  # Agrega a Mailchimp
            messages.success(request, "Email recibido. ¡Gracias!")
        except:
            messages.success(request, "Hubo un problema. Intentelo más tarde.")
        message = Mail(from_email='jmvazqueznicolas@gmail.com',
        to_emails=email,
        subject='Bievenido a mi boletin de noticias',
        html_content='<strong>Muchas gracias por suscribirte</strong>')
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY_NEW'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    return render(request, 'marketing/email_sus.html')

