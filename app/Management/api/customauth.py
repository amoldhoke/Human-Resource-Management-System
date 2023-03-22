from rest_framework.permissions import BasePermission

class IsRegularUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and not request.user.is_staff and not request.user.is_superuser
