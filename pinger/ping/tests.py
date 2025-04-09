from django.test import TestCase
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError
from .models import User, Alert, Notification, SafetyTip, AuditLog





class UserModelTest(TestCase):
    
    def test_user_creation(self):
        # Test that a user can be created with required fields
        user = User.objects.create_user(username='john_doe', password='password123')
        self.assertEqual(user.username, 'john_doe')
        self.assertTrue(user.check_password('password123'))
        
    def test_phone_number_nullable(self):
        # Test that phone_number can be null
        user = User.objects.create_user(username='janedoe', password='password123', phone_number=None)
        self.assertIsNone(user.phone_number)

    def test_department_nullable(self):
        # Test that department can be null
        user = User.objects.create_user(username='janedoe', password='password123', department=None)
        self.assertIsNone(user.department)





class AlertModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', password='password123')

    def test_alert_creation(self):
        # Test that an alert can be created with required fields
        alert = Alert.objects.create(
            category=Alert.Category.FIRE,
            location="Building A",
            severity=Alert.Severity.HIGH,
            status=Alert.Status.NEW,
            reported_by=self.user
        )
        self.assertEqual(alert.category, Alert.Category.FIRE)
        self.assertEqual(alert.severity, Alert.Severity.HIGH)
        self.assertEqual(alert.status, Alert.Status.NEW)

    def test_reported_by_constraint(self):
        # Test that reported_by cannot be null
        with self.assertRaises(IntegrityError):
            Alert.objects.create(
                category=Alert.Category.FIRE,
                location="Building B",
                severity=Alert.Severity.MEDIUM,
                status=Alert.Status.NEW
            )

    def test_acknowledged_by_nullable(self):
        # Test that acknowledged_by can be null
        alert = Alert.objects.create(
            category=Alert.Category.FIRE,
            location="Building C",
            severity=Alert.Severity.LOW,
            status=Alert.Status.NEW,
            reported_by=self.user,
            acknowledged_by=None
        )
        self.assertIsNone(alert.acknowledged_by)

    def test_foreign_key_relationship(self):
        # Test the ForeignKey relationship with 'User'
        alert = Alert.objects.create(
            category=Alert.Category.FIRE,
            location="Building D",
            severity=Alert.Severity.MEDIUM,
            status=Alert.Status.NEW,
            reported_by=self.user
        )
        self.assertEqual(alert.reported_by.username, 'john_doe')





class NotificationModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', password='password123')
        self.alert = Alert.objects.create(
            category=Alert.Category.FIRE,
            location="Building A",
            severity=Alert.Severity.HIGH,
            status=Alert.Status.NEW,
            reported_by=self.user
        )

    def test_notification_creation(self):
        # Test that a notification can be created
        notification = Notification.objects.create(
            alert=self.alert,
            recipient=self.user,
            medium=Notification.Medium.EMAIL,
            status=Notification.Status.PENDING
        )
        self.assertEqual(notification.medium, Notification.Medium.EMAIL)
        self.assertEqual(notification.status, Notification.Status.PENDING)

    def test_foreign_key_relationship(self):
        # Test the ForeignKey relationship with 'Alert' and 'User'
        notification = Notification.objects.create(
            alert=self.alert,
            recipient=self.user,
            medium=Notification.Medium.SMS,
            status=Notification.Status.SENT
        )
        self.assertEqual(notification.alert, self.alert)
        self.assertEqual(notification.recipient, self.user)





class SafetyTipModelTest(TestCase):

    def test_safety_tip_creation(self):
        # Test that a safety tip can be created
        safety_tip = SafetyTip.objects.create(
            category=SafetyTip.Category.PERSONAL,
            tips_note="Wear protective equipment.",
            tips_image="path_to_image.jpg"
        )
        self.assertEqual(safety_tip.category, SafetyTip.Category.PERSONAL)
        self.assertEqual(safety_tip.tips_note, "Wear protective equipment.")
        self.assertEqual(safety_tip.tips_image, "path_to_image.jpg")

    def test_image_required(self):
        # Test that image is required (cannot be blank or null)
        tip = SafetyTip(
            category=SafetyTip.Category.PERSONAL,
            tips_note="Wear protective equipment.",
            tips_image=None
        )
        with self.assertRaises(ValidationError):
            tip.full_clean()





class AuditLogModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='john_doe', password='password123')
        self.alert = Alert.objects.create(
            category=Alert.Category.FIRE,
            location="Building A",
            severity=Alert.Severity.HIGH,
            status=Alert.Status.NEW,
            reported_by=self.user
        )

    def test_audit_log_creation(self):
        # Test that an audit log can be created
        audit_log = AuditLog.objects.create(
            alert=self.alert,
            user=self.user,
            role=AuditLog.Role.ADMIN,
            action=AuditLog.Action.CREATED,
            ip_address="192.168.1.1",
            device_info="Chrome on Windows"
        )
        self.assertEqual(audit_log.role, AuditLog.Role.ADMIN)
        self.assertEqual(audit_log.action, AuditLog.Action.CREATED)
        self.assertEqual(audit_log.ip_address, "192.168.1.1")

    def test_foreign_key_relationship(self):
        # Test the ForeignKey relationship with 'Alert' and 'User'
        audit_log = AuditLog.objects.create(
            alert=self.alert,
            user=self.user,
            role=AuditLog.Role.SAFETY_OFFICER,
            action=AuditLog.Action.RESOLVED
        )
        self.assertEqual(audit_log.alert, self.alert)
        self.assertEqual(audit_log.user, self.user)
