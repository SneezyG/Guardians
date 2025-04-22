import factory
from django.contrib.auth import get_user_model
from .models import Alert, Notification, SafetyTip, AuditLog






class UserFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating user instances.
    This factory generates a User with basic fields and additional attributes
    such as phone number and department.
    """

    class Meta:
        model = get_user_model()
    
    username = factory.Faker('user_name')
    email = factory.Faker('email')
    phone_number = factory.Faker('phone_number')
    department = factory.Faker('street_name')
    password = factory.LazyAttribute(lambda obj: 'password123')
    
    @factory.post_generation
    def set_password(obj, create, extracted, **kwargs):
        """
        Post-generation hook to ensure the password is hashed.
        """

        if extracted:
            obj.set_password(extracted)
        else:
            obj.set_password('password123')
        obj.save()







class AlertFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Alert instances.
    This factory generates an Alert with random category, location, severity,
    status, and user-related fields.
    """

    class Meta:
        model = Alert
    
    category = factory.Faker('random_element', elements=[category.value for category in Alert.Category])
    location = factory.Faker('street_name')
    severity = factory.Faker('random_element', elements=[severity.value for severity in Alert.Severity])
    status = factory.Faker('random_element', elements=[status.value for status in Alert.Status])
    description_notes = factory.Faker('text')
    created_date = factory.Faker('date_time_this_year')
    reported_by = factory.SubFactory(UserFactory)
    confirmed_by = factory.SubFactory(UserFactory)
    resolution_notes = factory.Faker('text')
    resolved_by = factory.SubFactory(UserFactory)
    response_time = factory.Faker('random_int', min=1, max=120)








class NotificationFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating Notification instances.
    This factory generates a Notification linked to an Alert and a User, 
    and provides random medium, status, and sent time.
    """

    class Meta:
        model = Notification
    
    alert = factory.SubFactory(AlertFactory)
    recipient = factory.SubFactory(UserFactory)
    medium = factory.Faker('random_element', elements=[medium.value for medium in Notification.Medium])
    sent_at = factory.Faker('date_time_this_year')
    status = factory.Faker('random_element', elements=[status.value for status in Notification.Status])








class SafetyTipFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating SafetyTip instances.
    This factory generates a safety tip with a category, note, and image.
    An image path is simulated by using a fake file path.
    """

    class Meta:
        model = SafetyTip
    
    category = factory.Faker('random_element', elements=[category.value for category in SafetyTip.Category])
    tips_note = factory.Faker('paragraph')
    tips_image = factory.django.ImageField(filename='safety_tip_image.jpg', width=640, height=480)







class AuditLogFactory(factory.django.DjangoModelFactory):
    """
    Factory for creating AuditLog instances.
    This factory generates a log entry for a specific user action on an alert.
    It records the user role, action, and other audit-related information.
    """

    class Meta:
        model = AuditLog
    
    alert = factory.SubFactory(AlertFactory)
    user = factory.SubFactory(UserFactory)
    role = factory.Faker('random_element', elements=[role.value for role in AuditLog.Role])
    action = factory.Faker('random_element', elements=[action.value for action in AuditLog.Action])
    timestamp = factory.Faker('date_time_this_year')
    ip_address = factory.Faker('ipv4')
    device_info = factory.Faker('word')
