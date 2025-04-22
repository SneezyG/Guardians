import django_filters
from .models import Alert, AuditLog
from django.forms import DateInput




class AlertFilter(django_filters.FilterSet):
    """
    Add custom filter fields to alert API endpoint
    """

    created_date__gte = django_filters.DateFilter(
        field_name='created_date',
        lookup_expr='gte',
        label='Created After',
        widget=DateInput(attrs={'type': 'date'})
    )
    created_date__lte = django_filters.DateFilter(
        field_name='created_date',
        lookup_expr='lte',
        label='Created Before',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Alert
        fields = {
            'category': ['exact'],
            'location': ['icontains'],
            'severity': ['exact'],
            'status': ['exact'],
        }




class AuditLogFilter(django_filters.FilterSet):
    """
    Add custom filter fields to log API endpoint
    """

    timestamp__gte = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='gte',
        label='Timestamp After',
        widget=DateInput(attrs={'type': 'date'})
    )
    timestamp__lte = django_filters.DateFilter(
        field_name='timestamp',
        lookup_expr='lte',
        label='Timestamp Before',
        widget=DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = AuditLog
        fields = {
            'user__username': ['exact'],
            'role': ['exact'],
            'action': ['exact'],
            'alert__id': ['exact'],
            'alert__category': ['exact'],
            'alert__severity': ['exact'],
            'alert__location': ['icontains'],
        }
