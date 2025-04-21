from django.urls import path
from .views import (
    LogoutView,
    MyTokenObtainPairView,
    CreateAlertView,
    ListAlertsView,
    LatestAlertsView,
    AlertDetailView,
    UserAlertsView,
    UpdateAlertView,
    BulkUpdateAlertsView,
    AuditLogListView, 
    AuditLogReportView,
    SafetyTipListView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)




urlpatterns = [
    path('auth/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('alerts/', ListAlertsView.as_view(), name='list-alerts'),
    path('alerts/create', CreateAlertView.as_view(), name='create-alert'),
    path('alerts/latest/', LatestAlertsView.as_view(), name='latest-alerts'),
    path('alerts/<uuid:pk>/', AlertDetailView.as_view(), name='alert-detail'),
    path('alerts/user/<int:user_id>/', UserAlertsView.as_view(), name='user-alerts'),
    path('alerts/<uuid:pk>/update/', UpdateAlertView.as_view(), name='update-alert'),
    path('alerts/bulk/update/', BulkUpdateAlertsView.as_view(), name='bulk-update-alerts'),
    path('audit/', AuditLogListView.as_view(), name='audit-log-list'),
    path('audit/report/', AuditLogReportView.as_view(), name='audit-log-report'),
    path('safety_tips/', SafetyTipListView.as_view(), name='safety-tips-list'),
]
