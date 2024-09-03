# myapp/context_processors.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def google_maps_context(request):
    return {
        'GOOGLE_MAPS_API_KEY':  os.getenv('GOOGLE_MAPS_API_KEY'),
        'GOOGLE_MAPS_MAP_ID': os.getenv('GOOGLE_MAPS_MAP_ID'),
    }
