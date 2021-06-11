from rest_framework.permissions import BasePermission, SAFE_METHODS


class isAuthor(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Instance must have an attribute named `owner`.
        return obj.id == request.user.id


class isOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        # Instance must have an attribute named `owner`.
        return request.method == "GET" or obj.pemilik.id == request.user.id
