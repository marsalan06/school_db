from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError
from enum import Enum

class ErrorCodes(Enum):
    NOT_FOUND = 404
    SERVER_ERROR = 500
    FORBIDDEN = 403
    BAD_REQUEST = 400

class CustomErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
            
            
            if isinstance(response, HttpResponseNotFound):
                print(f"{ErrorCodes.NOT_FOUND.name} Error Detected")
                
                return render(
                    request,
                    'errors/404.html',
                    {'email_from_address': settings.EMAIL_FROM_ADDRESS},
                    status=ErrorCodes.NOT_FOUND.value
                )

            if response.status_code == ErrorCodes.SERVER_ERROR.value:
                print(f"{ErrorCodes.SERVER_ERROR.name} Error Detected")
                return render(
                    request,
                    'errors/500.html',
                    {'email_from_address': settings.EMAIL_FROM_ADDRESS},
                    status=ErrorCodes.SERVER_ERROR.value
                )

            if response.status_code == ErrorCodes.FORBIDDEN.value:
                print(f"{ErrorCodes.FORBIDDEN.name} Error Detected")
                return render(
                    request,
                    'errors/custom_403.html',
                    {'email_from_address': settings.EMAIL_FROM_ADDRESS},
                    status=ErrorCodes.FORBIDDEN.value
                )

            if response.status_code == ErrorCodes.BAD_REQUEST.value:
                print(f"{ErrorCodes.BAD_REQUEST.name} Error Detected")
                return render(
                    request,
                    'errors/custom_400.html',
                    {'email_from_address': settings.EMAIL_FROM_ADDRESS},
                    status=ErrorCodes.BAD_REQUEST.value
                )

            return response

        except Exception as e:
            print(f"Exception occurred: {e}") 
            return HttpResponseServerError(
                render(
                    request,
                    'errors/custom_error.html',
                    {'error': str(e), 'email_from_address': settings.EMAIL_FROM_ADDRESS},
                    status=ErrorCodes.SERVER_ERROR.value
                )
            )
