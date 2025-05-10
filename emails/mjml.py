import requests
from django.conf import settings
import os
from dotenv import load_dotenv
import json

load_dotenv()

MJML_APP_ID = os.getenv("MJML_APP_ID")
MJML_SECRET_KEY = os.getenv("MJML_SECRET_KEY")
MJML_API_URL = "https://api.mjml.io/v1/render"

def compile_mjml(mjml_content):
    """Sends MJML content to the MJML API and returns the compiled HTML."""
    
    auth = (MJML_APP_ID, MJML_SECRET_KEY)

    payload = {
        "mjml":mjml_content,
    }

    try:
        response = requests.post(MJML_API_URL, json=payload, auth=auth)
        response.raise_for_status()

        return response.json().get('html')

    except requests.exceptions.RequestException as e:
        # Handle request exceptions (network errors, etc.)
        print(f"Error calling MJML API: {e}")
        return None

def load_mjml_from_file(template_file):

    """ Load MJML content from file """
    full_path = os.path.join(settings.BASE_DIR, 'emails', 'templates', 'emails', template_file)
    try:
        with open(full_path, 'r', encoding='utf-8') as f:
            mjml_content = f.read()
        return mjml_content
    except Exception as e:
        print(f"Error loading MJML file: {e}")
        return None