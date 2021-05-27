from django.contrib import admin
from django.utils.safestring import mark_safe

from store.models import Bookmark, Category, Image, Product, Rating, Varian


class ImageInline(admin.TabularInline):
    model = Image
    fields = [
        'image',
        'is_thumb',
        
    ]
class VarianInline(admin.TabularInline):
    model = Varian
    fields = [
        'name',
        'stock',
        'price',
        'is_active',
      
        
    ]

class RatingInline(admin.TabularInline):
    model = Rating

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'penjual',
        'stock',
        'rating'
    )
    list_filter = ("category", )

    readonly_fields = (
        'slug',
        'sold',
        'create_at',
        'update',
        'price'
    )
    
    inlines = [ImageInline,VarianInline,RatingInline]

    def stock(self,obj):
        return obj.get_stock or 0
    
    def rating(self,obj):
        return obj.get_rating or 0

@admin.register(Varian)
class VarianAdmin(admin.ModelAdmin):
    inlines = [ImageInline]

admin.site.register(Category)
admin.site.register(Bookmark)
admin.site.register(Rating)
