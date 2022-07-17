from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthorOrAdminPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and (
            request.user.email == obj.email or request.user.is_staff
        )


class IsAuthorPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.email == obj.user.email


class DenyAll(BasePermission):
    def has_permission(self, request, view):
        return False

    def has_object_permission(self, request, view, obj):
        return False


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user or request.user.is_admin.filter(pk=request.user.pk).exists()