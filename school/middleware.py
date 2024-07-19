import json
import os
from django.http import HttpResponseForbidden
from django.contrib.sites.models import Site
from django.http import Http404
from .models import School


class SchoolDomainMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get the domain from the request
        host = request.get_host().split(':')[0]
        try:
            current_site = Site.objects.get(domain=host)
            request.site = current_site
            request.school = School.objects.get(domain=host)
        except Site.DoesNotExist:
            request.site = None
            request.school = None
        except School.DoesNotExist:
            request.school = None

        response = self.get_response(request)
        return response


class HostRestrictMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_hosts = self.load_allowed_hosts()

    def __call__(self, request):
        try:
            host = request.META.get('HTTP_HOST')
            print(f"Request host: {host}")  # Debugging line
            if host:
                host = host.split(':')[0]  # Get the host without the port
            else:
                host = ''

            if host not in self.allowed_hosts:
                print(f"Host {host} not allowed")  # Debugging line
                return HttpResponseForbidden("Forbidden: Host not allowed")
        except Exception as e:
            print(f"Error processing host: {e}")  # Debugging line
            return HttpResponseForbidden("Forbidden: Host not allowed")

        response = self.get_response(request)
        return response

    def load_allowed_hosts(self):
        # Assuming BASE_DIR is correctly set in your settings.py
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        allowed_hosts_file = os.path.join(BASE_DIR, 'allowed_hosts.json')

        try:
            with open(allowed_hosts_file) as f:
                data = json.load(f)
            return data.get('allowed_hosts', [])
        except (FileNotFoundError, json.JSONDecodeError) as e:
            # Handle error: log it or print it and return an empty list
            print(f"Error loading allowed hosts: {e}")
            return []
