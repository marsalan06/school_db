# myapp/context_processors.py
from django.conf import settings

def google_maps_context(request):
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY,
        'GOOGLE_MAPS_MAP_ID': settings.GOOGLE_MAPS_MAP_ID,
    }
