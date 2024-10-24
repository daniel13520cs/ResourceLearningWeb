from .models import VisitorLog
from django.utils.timezone import now

class LogIPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Get client's IP address
        ip_address = request.META.get('REMOTE_ADDR')
        
        # Check if IP exists, if not, create a new log
        visitor, created = VisitorLog.objects.get_or_create(ip_address=ip_address)
        if not created:
            visitor.last_visited = now()  # Update last visited timestamp
            visitor.save()

        response = self.get_response(request)
        return response
