from django.core.exceptions import ImproperlyConfigured
from rest_framework.filters import OrderingFilter

from django.core.exceptions import ImproperlyConfigured

class OrderCostomeFilter(OrderingFilter):
    ordering_fields = "__all__"
    def get_ordering(self, request, queryset, view):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.

        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.query_params.get(self.ordering_param)
        
        if params:
            fields = [param.strip() for param in params.split(',')]
            ordering = fields
            if ordering:
                return ordering
        return self.get_default_ordering(view)

    def get_default_ordering(self, view):
        ordering = getattr(view, 'ordering', None)
        if isinstance(ordering, str):
            return (ordering,)
        return ordering

    def remove_invalid_fields(self, queryset, fields, view,request ={}):
        ordering_fields = getattr(view, 'ordering_fields', self.ordering_fields)
        
        if not ordering_fields == '__all__':
        
            serializer_class = getattr(view, 'serializer_class', None)
            if serializer_class is None:
                serializer_class = view.get_serializer_class()
            if serializer_class is None:
                msg = ("Cannot use %s on a view which does not have either a "
                       "'serializer_class' or 'ordering_fields' attribute.")
                raise ImproperlyConfigured(msg % self.__class__.__name__)
        

        if ordering_fields is None:
            # Default to allowing filtering on serializer field names (return field sources)
            valid_fields = [
                (field.source, field_name)
                for field_name, field in serializer_class().fields.items()
                if not getattr(field, 'write_only', False)
            ]
            return [term[0] for term in valid_fields if term[0] != "*"]
        elif ordering_fields == '__all__':
            # View explicitly allows filtering on any model field
            valid_fields = [field.name for field in queryset.model._meta.fields]
            valid_fields += queryset.query.aggregates.keys()
            return [term for term in fields if term.lstrip('-') in valid_fields]
        else:
            # Allow filtering on defined field name (return field sources)
            valid_fields = [
                (field.source, field_name)
                for field_name, field in serializer_class().fields.items()
                if not getattr(field, 'write_only', False)
            ]
            return [term[0] for term in valid_fields if term[0] != "*" and term[1].lstrip('-') in fields]

    def filter_queryset(self, request, queryset, view):
        ordering = self.get_ordering(request, queryset, view)
        
        print(ordering)
        if ordering:
            return queryset.order_by(*ordering)

        return queryset
