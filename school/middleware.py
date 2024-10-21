import json
import os
from django.http import HttpResponseForbidden
from django.contrib.sites.models import Site
from django.http import Http404
from .models import School
from django.shortcuts import render


import json
import os
from django.http import HttpResponseForbidden
from django.contrib.sites.models import Site
from django.core.cache import cache
from django.utils.deprecation import MiddlewareMixin
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class HostRestrictMiddleware(MiddlewareMixin):
    CACHE_KEY = 'allowed_hosts'
    CACHE_TIMEOUT = 300  # Cache for 5 minutes

    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        allowed_hosts = self.get_allowed_hosts()

        if host not in allowed_hosts:
            # Optionally log the forbidden access attempt
            return render(request, 'domain_not_found.html', status=404)

        response = self.get_response(request)
        return response

    def get_allowed_hosts(self):
        allowed_hosts = cache.get(self.CACHE_KEY)
        if allowed_hosts is None:
            # Fetch from the Sites table
            sites = Site.objects.values_list('domain', flat=True)
            allowed_hosts = [site.lower() for site in sites]
            cache.set(self.CACHE_KEY, allowed_hosts, self.CACHE_TIMEOUT)
        return allowed_hosts


@receiver([post_save, post_delete], sender=Site)
def invalidate_allowed_hosts_cache(sender, **kwargs):
    cache.delete(HostRestrictMiddleware.CACHE_KEY)


class SchoolDomainMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        super().__init__(get_response)

    def __call__(self, request):
        host = request.get_host().split(':')[0].lower()
        try:
            current_site = Site.objects.get(domain__iexact=host)
            request.site = current_site
            request.school = School.objects.get(domain__iexact=host)
        except Site.DoesNotExist:
            request.site = None
            request.school = None
        except School.DoesNotExist:
            request.school = None

        if request.school is None:
            # Render the custom "School Not Found" page with a 404 status
            return render(request, 'school_not_found.html', status=404)

        response = self.get_response(request)
        return response
