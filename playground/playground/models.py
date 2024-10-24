from django.db import models

class VisitorLog(models.Model):
    ip_address = models.GenericIPAddressField()
    last_visited = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.ip_address