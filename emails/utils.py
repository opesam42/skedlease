from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import engines
from .mjml import *


def send_welcome_email(to_email, context={}):
    """ Send email verification to user """

    # current_site = get_current_site(request)
    subject = "Welcome to SkedlEase"
    mjml_content = load_mjml_from_file('welcome.mjml')

    # pass context 
    django_engines = engines['django']
    template = django_engines.from_string(mjml_content)
    rendered_mjml = template.render(context)


    html_content = compile_mjml(rendered_mjml)


    try:
        email = EmailMessage(
            subject=subject,
            body=html_content,
            from_email=settings.EMAIL_HOST_USER,
            to=[to_email],
        )
        email.content_subtype = "html"
        email.encoding = 'utf-8'
        email.send()
        print('email sent')
        return True
    
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
