from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


# class FullDjangoModelPermissions(permissions.DjangoModelPermissions):
#     def __init__(self) -> None:
#         self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']

# class ViewCustomerHistoryPermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.has_perm('store.view_history')


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission class to allow owners to edit their own objects.
    """

    def has_object_permission(self, request, view, obj):
        # Allow read-only permissions for all requests
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the user is the owner of the object
        return obj.owner == request.user


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS requests for all users
        if request.method in permissions.SAFE_METHODS:
            return True

        # Check if the requesting user is the author of the post
        return obj.author == request.user.author
