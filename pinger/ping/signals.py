
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Alert, AuditLog
from django.contrib.auth.models import Group
from threading import local







_request_local = local()

def set_current_request(request):
    _request_local.request = request



def get_current_request():
    return getattr(_request_local, 'request', None)



def get_user_role(user):
    """
    Try to infer the AuditLog.Role from the user's group or permissions.
    """
    if user.is_superuser:
        return AuditLog.Role.ADMIN

    group_roles = {
        'worker': AuditLog.Role.WORKER,
        'safety_officer': AuditLog.Role.SAFETY_OFFICER,
        'admin': AuditLog.Role.ADMIN,
        'agent': AuditLog.Role.AGENT,
    }

    for group in user.groups.all():
        role = group_roles.get(group.name.lower())
        if role:
            return role

    return AuditLog.Role.WORKER  # Default fallback







@receiver(pre_save, sender=Alert)
def track_old_instance(sender, instance, **kwargs):
    """
    A pre-save signal on alert model that save old alert object as an attribute
    on the new instance. 
    """

    if instance.pk:
        try:
            # Retrieve the old instance (before save)
            instance._old_instance = Alert.objects.get(pk=instance.pk)
        except Alert.DoesNotExist:
            instance._old_instance = None
    else:
        # If this is a new instance, no old instance attributes
        instance._old_instance = None







@receiver(post_save, sender=Alert)
def log_alert_status_change(sender, instance, created, **kwargs):
    """
    A post-save signal on alert model that log & broadcast actions(status changes) 
    on alert instances.
    """

    request = get_current_request()
    user = getattr(request, 'user', None)
    ip = request.META.get('REMOTE_ADDR') if request else None
    device = request.META.get('HTTP_USER_AGENT') if request else None

    if not user or not user.is_authenticated:
        return

    # Infer role from user
    role = get_user_role(user)

    # If the instance is new, log it as CREATED
    if created:
        AuditLog.objects.create(
            alert=instance,
            user=user,
            role=role,
            action=AuditLog.Action.CREATED,
            ip_address=ip,
            device_info=device
        )
        return

    # If the old instance exists, compare statuses
    old_instance = instance._old_instance
    if old_instance is None:
        return

    # No change in status, so no need to log
    if old_instance.status == instance.status:
        return

    # Define status-to-action mapping
    status_to_action = {
        Alert.Status.RESOLVED: AuditLog.Action.RESOLVED,
        Alert.Status.ESCALATED: AuditLog.Action.ESCALATED,
        Alert.Status.DISMISSED: AuditLog.Action.DISMISSED,
        Alert.Status.CONFIRMED: AuditLog.Action.CONFIRMED,
    }

    action = status_to_action.get(instance.status)
    if not action:
        return

    # Log the status change
    AuditLog.objects.create(
        alert=instance,
        user=user,
        role=role,
        action=action,
        ip_address=ip,
        device_info=device
    )

    # Broadcast the update




