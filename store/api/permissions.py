from rest_framework.permissions import BasePermission

class IsAuthorOrReadonly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.penjual.id == request.user.id or request.method == "GET"

class IsRatingAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        """ 
            for rating detail
            only store owner and rating owner can crud
            
                    owner rating                                store owner 
        """
        return obj.user.id == request.user.id or obj.product.penjual.id == request.user.id