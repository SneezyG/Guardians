from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import Alert, AuditLog, SafetyTip





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Add custom attribute to users token at authentication
    """

    def validate(self, attrs):
        data = super().validate(attrs)

        data['username'] = self.user.username
        data['email'] = self.user.email
        data['groups'] = list(self.user.groups.values_list('name', flat=True))

        return data






class AlertSerializer(serializers.ModelSerializer):
    """
    Add custom attribute to alert instances at API endpoint    
    """

    reported_by_username = serializers.CharField(source='reported_by.username', read_only=True)
    confirmed_by_username = serializers.CharField(source='confirmed_by.username', read_only=True)
    resolved_by_username = serializers.CharField(source='resolved_by.username', read_only=True)

    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ['reported_by']




class AuditLogSerializer(serializers.ModelSerializer):
    """
    Add custom attribute to log instances at API endpoint 
    """
    user_name = serializers.CharField(source='user.username', read_only=True)
    alert_id = serializers.CharField(source='alert.id', read_only=True)
    alert_category = serializers.CharField(source='alert.category', read_only=True)
    alert_severity = serializers.CharField(source='alert.severity', read_only=True)
    alert_location = serializers.CharField(source='alert.location', read_only=True)

    class Meta:
        model = AuditLog
        fields = '__all__'





class SafetyTipSerializer(serializers.ModelSerializer):
    """
    Includes all safety-tips attributes for instances at API endpoint
    """
    class Meta:
        model = SafetyTip
        fields = '__all__'
