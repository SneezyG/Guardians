from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import Alert, Notification, SafetyTip, AuditLog





@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    """
    Admin interface customization for Django's built-in LogEntry model.
    Provides an audit trail for admin actions with filtering, search, and display enhancements.
    """
    list_display = (
        'action_time',
        'user',
        'content_type',
        'object_repr',
        'action_flag',
        'change_message',
    )
    list_filter = (
        'action_flag',
        'user',
        'content_type',
    )
    search_fields = (
        'object_repr',
        'change_message',
        'user__username',
    )
    date_hierarchy = 'action_time'
    ordering = ['-action_time']

    def has_add_permission(self, request):
        return False  # Log entries should not be added manually

    def has_change_permission(self, request, obj=None):
        return False  # Prevent changes for integrity

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletes for integrity





# Get the custom User model
User = get_user_model()

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom admin interface for the User model, adding useful features like filters, actions, and a clean layout.
    """
    list_display = (
        'username', 'email', 'phone_number', 'department', 'is_active', 'is_staff', 'last_login', 'date_joined'
    )
    list_filter = ('is_active', 'is_staff', 'groups')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ['username']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number', 'department')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'phone_number', 'is_staff', 'is_active'),
        }),
    )
    
    actions = ['suspend_user', 'activate_user']

    def suspend_user(self, request, queryset):
        """Action to suspend selected users."""
        queryset.update(is_active=False)
        self.message_user(request, "Selected users have been suspended.")

    def activate_user(self, request, queryset):
        """Action to activate selected users."""
        queryset.update(is_active=True)
        self.message_user(request, "Selected users have been activated.")

    suspend_user.short_description = "Suspend users"
    activate_user.short_description = "Activate users"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('date_joined', 'last_login')  # Prevent modification of dates after creation
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj and obj.is_superuser:
            return False  # Prevent changes to superusers
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletes to users record  





@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Alert model. Provides quick filtering, searching, 
    and actions to manage alerts, including resolution and escalation.
    """
    list_display = (
        'id', 'category', 'severity', 'status', 'created_date', 'reported_by', 'confirmed_by', 'resolved_by'
    )
    list_filter = (
        'category', 'severity', 'status', 'created_date', 'reported_by', 'confirmed_by', 'resolved_by'
    )
    search_fields = ('description_notes', 'location', 'reported_by__email', 'acknowledged_by__email')
    date_hierarchy = 'created_date'
    ordering = ['-created_date']
    
    actions = ['resolve_alert', 'escalate_alert', 'dismissed_alert']

    def resolve_alert(self, request, queryset):
        """Action to resolve selected alerts."""
        queryset.update(status=Alert.Status.RESOLVED)
        self.message_user(request, "Selected alerts have been resolved.")

    def escalate_alert(self, request, queryset):
        """Action to escalate selected alerts."""
        queryset.update(status=Alert.Status.ESCALATED)
        self.message_user(request, "Selected alerts have been escalated.")

    def dismissed_alert(self, request, queryset):
        """Action to dismissed selected alerts."""
        queryset.update(status=Alert.Status.DISMISSED)
        self.message_user(request, "Selected alerts have been dismissed.")

    resolve_alert.short_description = "Resolve selected alerts"
    escalate_alert.short_description = "Escalate selected alerts"
    dismissed_alert.short_description = "Dismissed selected alerts"

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('created_date',)  # Prevent modification of 'created_date' after creation
        return self.readonly_fields

    def has_change_permission(self, request, obj=None):
        if obj and obj.status == Alert.Status.RESOLVED:
            return False  # Prevent changes to resolved alerts
        return super().has_change_permission(request, obj)





@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Notification model. Provides filters, actions,
    and a clean layout for managing notifications related to alerts.
    """
    list_display = (
        'id', 'alert', 'recipient', 'medium', 'sent_at', 'status'
    )
    list_filter = (
        'status', 'medium', 'sent_at', 'recipient'
    )
    search_fields = ('alert__id', 'recipient__email', 'medium')
    date_hierarchy = 'sent_at'
    ordering = ['-sent_at']
    
    actions = ['mark_as_sent', 'mark_as_failed']

    def mark_as_sent(self, request, queryset):
        """Action to mark selected notifications as 'Sent'."""
        queryset.update(status=Notification.Status.SENT)
        self.message_user(request, "Selected notifications have been marked as Sent.")

    def mark_as_failed(self, request, queryset):
        """Action to mark selected notifications as 'Failed'."""
        queryset.update(status=Notification.Status.FAILED)
        self.message_user(request, "Selected notifications have been marked as Failed.")

    mark_as_sent.short_description = "Mark selected notifications as Sent"
    mark_as_failed.short_description = "Mark selected notifications as Failed"

    def has_add_permission(self, request):
        return False  # Notifications should not be added manually

    def has_change_permission(self, request, obj=None):
        return False  # Prevent changes for integrity





@admin.register(SafetyTip)
class SafetyTipAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Safety model. Provides filters, actions,
    and an interactive layout for managing safety tips across different categories.
    """
    list_display = (
        'id', 'category', 'tips_note', 'tips_image'
    )
    list_filter = (
        'category',
    )
    search_fields = ('tips_note', 'category')





@admin.register(AuditLog)
class AuditAdmin(admin.ModelAdmin):
    """
    Custom admin interface for the Audit model. Provides filters, actions,
    and an interactive layout for reviewing alert activity logs.
    """
    list_display = (
        'id', 'alert', 'user', 'role', 'action', 'timestamp', 'ip_address'
    )
    list_filter = (
        'action', 'role', 'user', 'timestamp'
    )
    search_fields = ('alert__id', 'user__email', 'action', 'ip_address')
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']

    def has_add_permission(self, request):
        return False  # Log entries should not be added manually

    def has_change_permission(self, request, obj=None):
        return False  # Prevent changes for integrity

    def has_delete_permission(self, request, obj=None):
        return False  # Prevent deletes for integrity


