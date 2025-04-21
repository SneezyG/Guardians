from rest_framework import permissions




class IsAdminSafetyOrSuper(permissions.BasePermission):
    """
    Allows access to users who are:
    - In the 'admin' or 'safety_officer' group
    - OR a Django superuser (is_superuser = True)
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.is_superuser or
                request.user.groups.filter(name__in=['admin', 'safety_officer']).exists()
            )
        )
