import requests
from django.conf import settings
import requests
from geopy.geocoders import Nominatim


def fetch_news_and_events_from_lms(organization_id):
    # Construct the URL. Make sure to replace `lms:8001` with the correct hostname and port as needed.
    url = f'{settings.LMS_SERVER_URL}/api/news-and-events/{organization_id}/'
    print(organization_id)
    try:
        response = requests.get(url)
        # Raises an HTTPError if the response status code is 4XX/5XX
        response.raise_for_status()
        print(response.json())
        return response.json()  # Returns the JSON response
    except requests.exceptions.RequestException as e:
        # Handle any errors that occur during the request sending/receiving process
        print(f"An error occurred: {e}")
        return None


def update_lat_lon(modeladmin, request, queryset):
    geolocator = Nominatim(user_agent="school")  # Replace 'school' with your app's name

    for organization in queryset:
        if organization.address:
            location = geolocator.geocode(organization.address)
            if location:
                organization.latitude = location.latitude
                organization.longitude = location.longitude
                organization.save()

    modeladmin.message_user(request, "Latitude and Longitude updated successfully.")

update_lat_lon.short_description = "Update latitude and longitude from address"

             