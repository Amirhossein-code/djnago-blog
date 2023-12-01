from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class IsAuthorOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an author profile to access it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user making the request is the owner of the author profile
        return obj.user == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Restrict write access to the post author
        if request.user.is_authenticated and obj.author == request.user:
            return True

        return False
