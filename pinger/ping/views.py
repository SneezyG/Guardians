from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import generics, permissions, status
from django.utils import timezone
from .models import Alert, AuditLog, SafetyTip
from .permissions import IsAdminSafetyOrSuper
from .serializers import MyTokenObtainPairSerializer, AlertSerializer, AuditLogSerializer
from django_filters.rest_framework import DjangoFilterBackend
from .filters import AlertFilter, AuditLogFilter





class LogoutView(APIView):
    """
    Invalidate the user token, logging out the user 
    """
    
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)




class MyTokenObtainPairView(TokenObtainPairView):
    """
    A custom view that extent the built in TokenObtainPairView provided by
    rest_framework_simplejwt for user authentication.
    """

    serializer_class = MyTokenObtainPairSerializer





class ListAlertsView(generics.ListAPIView):
    """
    GET /alerts
    List all alerts, with optional search by category, location, or notes.

    Access: Admin, Safety, and Super Users only
    """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAdminSafetyOrSuper]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AlertFilter




class CreateAlertView(generics.CreateAPIView):
    """
    POST /alerts/create
    Create a new alert.

    Access: Authenticated Users
    Automatically sets the 'reported_by' field to the currently authenticated user.
    """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Assign the authenticated user as the reporter of the alert.
        """
        serializer.save(reported_by=self.request.user)





class LatestAlertsView(generics.ListAPIView):
    """
    GET /alerts/latest
    Retrieve alerts created today.

    Access: Any Authenticated User
    """

    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Return alerts whose creation date is today.
        """
        today = timezone.now().date()
        return Alert.objects.filter(created_date__date=today)





class AlertDetailView(generics.RetrieveAPIView):
    """
    GET /alerts/<uuid:pk>
    Retrieve a single alert by its ID.

    Access: Any Authenticated User
    """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]





class UserAlertsView(generics.ListAPIView):
    """
    GET /alerts/user/<user_id>
    Retrieve all alerts reported by a specific user.

    Access: Any Authenticated User
    """

    serializer_class = AlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """
        Filter alerts by the 'reported_by' user ID passed in the URL.
        """
        user_id = self.kwargs['user_id']
        return Alert.objects.filter(reported_by__id=user_id)





class UpdateAlertView(generics.UpdateAPIView):
    """
    PUT /alerts/<uuid:pk>/update
    Update an alert's details.

    Access: Admin, Safety, and Super Users only
    """

    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAdminSafetyOrSuper]





class BulkUpdateAlertsView(APIView):
    """
    PUT /alerts/bulk/update
    Update multiple alerts in a single request.

    Expects a payload like:
    {
        "alerts": [
            {"id": "uuid1", "status": "resolved"},
            {"id": "uuid2", "status": "dismissed"}
        ]
    }

    Access: Admin, Safety, and Super Users only
    """

    permission_classes = [IsAdminSafetyOrSuper]

    def put(self, request):
        """
        Iterate over provided alert updates and apply changes.
        Skips alerts that don't exist or are missing an 'id'.
        """

        alerts_data = request.data.get('alerts', [])
        updated = []

        for alert_data in alerts_data:
            alert_id = alert_data.get('id')
            if alert_id:
                try:
                    alert = Alert.objects.get(id=alert_id)
                    for field, value in alert_data.items():
                        if field != 'id':
                            setattr(alert, field, value)
                    alert.save()
                    updated.append(alert)
                except Alert.DoesNotExist:
                    continue

        return Response(AlertSerializer(updated, many=True).data, status=status.HTTP_200_OK)





class AuditLogListView(generics.ListAPIView):
    """
    GET /audit
    List all logs on alerts, with optional search by action, user-role, user-name, 
    timestamp and alert-id.

    Access: Admin, Safety, and Super Users only
    """

    queryset = AuditLog.objects.select_related('user', 'alert').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminSafetyOrSuper]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuditLogFilter





class AuditLogReportView(generics.ListAPIView):
    """
    GET /audit/report
    Generate a log report of all alert, with optional search by action, user-role, user-name, 
    timestamp and alert-id.

    Access: Admin, Safety, and Super Users only
    """

    queryset = AuditLog.objects.select_related('user', 'alert').all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminSafetyOrSuper]
    filter_backends = [DjangoFilterBackend]
    filterset_class = AuditLogFilter

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        return Response({
            "total_logs": queryset.count(),
            "report": AuditLogSerializer(queryset, many=True).data
        })




class SafetyTipListView(generics.ListAPIView):
    """
    GET /safety_tips
    Get the latest safety tips

    Access: Any Authenticated User
    """

    queryset = SafetyTip.objects.all()
    serializer_class = SafetyTipSerializer
    permission_classes = [IsAuthenticated]