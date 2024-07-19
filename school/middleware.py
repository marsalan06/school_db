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
