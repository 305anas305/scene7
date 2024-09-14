from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponse

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        if request.user.is_authenticated:
            response['Cache-Control'] = 'no-store'
            response['Pragma'] = 'no-cache'
        return response