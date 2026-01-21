from rest_framework import permissions


class IsProductOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of a product to edit or delete it.
    """
    
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed for any authenticated user
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner of the product
        return obj.added_by == request.user
