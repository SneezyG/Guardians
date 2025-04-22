import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser





class User(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Add two custom fields: phone_number & department
    """

    phone_number = models.CharField(
        max_length=30,
        verbose_name="Phone Number",
        null=True,
        blank=True
    )

    department = models.CharField(
        max_length=30,
        verbose_name="Department Block",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.username}".capitalize()

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['first_name', 'last_name']





class Alert(models.Model):
    """
    Represents an alert raised in the system. This includes information 
    about the nature of the alert, the location, severity, status, 
    description, and resolution. It also tracks the users involved in 
    acknowledging and resolving the alert.
    """

    class Category(models.TextChoices):
        FIRE = 'fire', 'Fire'
        ELECTRICAL = 'electrical', 'Electrical'
        CHEMICAL = 'chemical', 'Chemical'
        ACCIDENT = 'accident', 'Accident'
        INCIDENT = 'incident', 'Incident'
        OTHER = 'other', 'Other'

    class Severity(models.TextChoices):
        LOW = 'low', 'Low'
        MEDIUM = 'medium', 'Medium'
        HIGH = 'high', 'High'
        CRITICAL = 'critical', 'Critical'

    class Status(models.TextChoices):
        NEW = 'new', 'New'
        DISMISSED = 'dismissed', 'Dismissed'
        CONFIRMED = 'confirmed', 'Confirmed'
        RESOLVED = 'resolved', 'Resolved'
        ESCALATED = 'escalated', 'Escalated'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Alert ID",
        null=False,
        blank=False
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        verbose_name="Alert Type",
        null=False,
        blank=False
    )

    location = models.CharField(
        max_length=30,
        verbose_name="Alert Location",
        null=False,
        blank=False
    )

    severity = models.CharField(
        max_length=10,
        choices=Severity.choices,
        verbose_name="Severity Level",
        null=False,
        blank=False
    )

    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.NEW,
        verbose_name="Alert Status",
        null=False,
        blank=False
    )

    description_notes = models.TextField(
        verbose_name="Description and Notes",
        null=True,
        blank=True
    )

    created_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Alert Creation Date",
        null=False,
        blank=False
    )

    reported_by = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name="alerts_reported",
        verbose_name="Reported By",
        null=False,
        blank=False
    )

    confirmed_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        related_name="alerts_confirmed",
        verbose_name="Confirmed By",
        null=True,
        blank=True
    )

    resolution_notes = models.TextField(
        verbose_name="Resolution Notes",
        null=True,
        blank=True
    )

    resolved_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        related_name="alerts_resolved",
        verbose_name="Resolved By",
        null=True,
        blank=True
    )

    response_time = models.IntegerField(
        verbose_name="Response Time (minutes)",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Alert {self.id} - {self.category} at {self.location}"

    class Meta:
        verbose_name = "Alert"
        verbose_name_plural = "Alerts"
        ordering = ['-created_date']





class Notification(models.Model):
    """
    Represents a notification sent to a user about a specific alert.
    Tracks delivery medium, time, recipient, and status of the notification.
    """

    class Medium(models.TextChoices):
        EMAIL = 'email', 'Email'
        SMS = 'sms', 'SMS'

    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        SENT = 'sent', 'Sent'
        FAILED = 'failed', 'Failed'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Notification ID",
        null=False,
        blank=False
    )

    alert = models.ForeignKey(
        'Alert',
        on_delete=models.CASCADE,
        related_name="notifications",
        verbose_name="Related Alert",
        null=False,
        blank=False
    )

    recipient = models.ForeignKey(
        'User',
        on_delete=models.CASCADE,
        related_name="notifications_received",
        verbose_name="Notification Recipient",
        null=False,
        blank=False
    )

    medium = models.CharField(
        max_length=10,
        choices=Medium.choices,
        verbose_name="Notification Medium",
        null=False,
        blank=False
    )

    sent_at = models.DateTimeField(
        verbose_name="Time Sent",
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name="Notification Status",
        null=False,
        blank=False
    )

    def __str__(self):
        return f"Notification to {self.recipient} via {self.medium}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-sent_at']






class SafetyTip(models.Model):
    """
    Represents a safety tip provided within the system.
    Each tip is categorized to assist users in understanding various safety areas
     and best practices.
    An optional image illustration can be associated with each tip.
    """

    class Category(models.TextChoices):
        PERSONAL = 'personal', 'Personal'
        MACHINERY = 'machinery', 'Machinery'
        HAZARDS = 'hazards', 'Hazards'
        FIRE = 'fire', 'Fire'
        SLIPS = 'slips', 'Slips'
        HANDLING = 'handling', 'Handling'
        EMERGENCY = 'emergency', 'Emergency'
        WORKPLACE = 'workplace', 'Workplace'
        SUPERVISION = 'supervision', 'Supervision'
        BEHAVIOR = 'behavior', 'Behavior'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Safety Tip ID",
        null=False,
        blank=False
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        verbose_name="Tip Category",
        null=False,
        blank=False
    )

    tips_note = models.TextField(
        verbose_name="Safety Tip Notes",
        null=False,
        blank=False
    )

    tips_image = models.ImageField(
        upload_to='safety_tips_images/',
        verbose_name="Tip Illustration Image",
        null=False,
        blank=False
    )

    def __str__(self):
        return f"{self.get_category_display()} Tip"

    class Meta:
        verbose_name = "Safety Tip"
        verbose_name_plural = "Safety Tips"
        ordering = ['category']





class AuditLog(models.Model):
    """
    Represents a log entry for user actions on alerts. Tracks who performed what action, 
    their role, the device used, and when the action took place. Useful for auditing and 
    security tracking.
    """

    class Role(models.TextChoices):
        WORKER = 'worker', 'Worker'
        SAFETY_OFFICER = 'safety_officer', 'Safety Officer'
        ADMIN = 'admin', 'Admin'
        AGENT = 'agent', 'Agent'

    class Action(models.TextChoices):
        CREATED = 'created', 'Created'
        DISMISSED = 'dismissed', 'Dismissed'
        CONFIRMED = 'confirmed', 'Confirmed'
        RESOLVED = 'resolved', 'Resolved'
        ESCALATED = 'escalated', 'Escalated'
        

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="Audit Log ID",
        null=False,
        blank=False
    )

    alert = models.ForeignKey(
        'Alert',
        on_delete=models.PROTECT,
        related_name="audit_logs",
        verbose_name="Related Alert",
        null=False,
        blank=False
    )

    user = models.ForeignKey(
        'User',
        on_delete=models.PROTECT,
        related_name="audit_logs",
        verbose_name="User",
        null=False,
        blank=False
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        verbose_name="User Role",
        null=False,
        blank=False
    )

    action = models.CharField(
        max_length=20,
        choices=Action.choices,
        verbose_name="Action Performed",
        null=False,
        blank=False
    )

    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Action Timestamp",
        null=False,
        blank=False
    )

    ip_address = models.GenericIPAddressField(
        verbose_name="IP Address",
        null=True,
        blank=True
    )

    device_info = models.TextField(
        verbose_name="Device Information",
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.user} {self.action} alert {self.alert.id} at {self.timestamp}"

    class Meta:
        verbose_name = "Audit Log"
        verbose_name_plural = "Audit Logs"
        ordering = ['-timestamp']
