from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminOrAuthenticatedReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            (
                request.method in SAFE_METHODS
                and request.user.is_authenticated
                and request.user
            )
            or (request.user and request.user.is_staff)
        )
