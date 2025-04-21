import django_filters
from .models import Alert, AuditLog




class AlertFilter(django_filters.FilterSet):
    """
    Add custom filter fields to alert API endpoint
    """

    class Meta:
        model = Alert
        fields = {
            'category': ['exact'],
            'location': ['icontains'],
            'severity': ['exact'],
            'status': ['exact'],
            'created_date': ['lte', 'gte'],
        }




class AuditLogFilter(django_filters.FilterSet):
    """
    Add custom filter fields to log API endpoint
    """

    class Meta:
        model = AuditLog
        fields = {
            'user__username': ['exact'],
            'role': ['exact'],
            'action': ['exact'],
            'alert__id': ['exact'],
            'alert__category': ['exact'],
            'alert__severity': ['exact'],
            'alert__location': ['icontain'],
            'timestamp': ['lte', 'gte'],
        }
