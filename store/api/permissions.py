from rest_framework.permissions import BasePermission

class IsAuthorOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return "GET" in request.method or obj.penjual == request.user