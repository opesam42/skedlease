from django.shortcuts import render
from .mjml import *
from django.conf import settings
from django.http import JsonResponse

# Create your views here.
def welcome(request):


    mjml_content = load_mjml_from_file('welcome.mjml')

    html_content = compile_mjml(mjml_content)
    
    if html_content:
        # Example: Send the HTML content as part of a response
        print({"html": html_content})
    else:
        print({"error": "Failed to compile MJML"})
    
    return render(request, 'emails/welcome.html')