from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    Read permissions are allowed to any request.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Support both 'owner' and 'reviewer' as owner fields
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        if hasattr(obj, 'reviewer'):
            return obj.reviewer == request.user
        return False


class IsOwnerOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to view or edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Check if the user is the owner of the profile
        return obj.user == request.user


class CanReviewUser(permissions.BasePermission):
    """
    Custom permission to only allow users to review other users.
    Prevents users from reviewing themselves.
    """

    def has_permission(self, request, view):
        # Only check for non-safe methods like POST
        if request.method in permissions.SAFE_METHODS:
            return True

        # Get reviewee ID from request data
        reviewee_id = request.data.get('reviewee')
        if not reviewee_id:
            return False

        # Don't allow users to review themselves
        return str(request.user.id) != str(reviewee_id)