from rest_framework.permissions import BasePermission


class IsReviewOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow GET, HEAD, and OPTIONS requests.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Check if the request user is the owner of the review.
        return obj.user == request.user
