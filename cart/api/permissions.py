from rest_framework.permissions import BasePermission


class IsCartAuth(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.cart.user.id == request.user.id
