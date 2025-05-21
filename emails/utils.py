from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.template import engines
from .mjml import *


class EmailSender:
    def __init__(self, to_email, email_subject, template_path, context=None):
        self.to_email = to_email
        self.email_subject = email_subject
        self.template_path = template_path
        self.context = context or {}

    def send(self):
        try:
            # subject = "Welcome to SkedlEase"
            mjml_content = load_mjml_from_file(self.template_path)

            # pass context 
            django_engines = engines['django']
            template = django_engines.from_string(mjml_content)
            rendered_mjml = template.render(self.context)

            html_content = compile_mjml(rendered_mjml)

            email = EmailMessage(
                subject=self.email_subject,
                body=html_content,
                from_email=settings.EMAIL_HOST_USER,
                to=[self.to_email],
            )
            email.content_subtype = "html"
            email.encoding = 'utf-8'
            email.send()
            print('email sent')
            return True
        
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
        
def send_patient_welcome_email(to_email, context={}):
    return EmailSender(
        to_email=to_email,
        email_subject="Welcome to Skedlease",
        template_path='welcome.mjml',
        context=context,
    ).send()

def send_doctor_welcome_email(to_email, context={}):
    return EmailSender(
        to_email=to_email,
        email_subject="Doctor!, Welcome to Skedlease",
        template_path='doctor_welcome.mjml',
        context=context,
    ).send()