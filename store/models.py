from django.db import models
from django.db.models import Avg, Min

from django.conf import settings
from django.utils.translation import ugettext_lazy as _

from django.core.validators import MinValueValidator, MaxValueValidator
from costumer.models import Store

# Create your models here.


class Category(models.Model):
    content = models.CharField(max_length=70)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.content


class Image(models.Model):
    product = models.ForeignKey(
        "Product",
        related_name="images",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    varian = models.ForeignKey(
        "Varian",
        related_name="image_varian",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    image = models.ImageField(
        upload_to="product", height_field="height_field", width_field="width_field"
    )
    height_field = models.PositiveIntegerField(default=0)
    width_field = models.PositiveIntegerField(default=0)
    is_thumb = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"image for {self.product.title if self.product else self.varian.name}"


class Varian(models.Model):
    product = models.ForeignKey(
        "Product", related_name="varian", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    price = models.IntegerField(
        _(" price in IDR"),
        validators=[MaxValueValidator(99999999), MinValueValidator(0)],
    )

    def __str__(self) -> str:
        return f"varian {self.  product.title} name {self.name}"

    def get_image_varian(self):
        return self.image_varian.all() or None
    
    def get_order_item(self):
        return self.product_order.select_related('order').all()


class Product(models.Model):
    penjual = models.ForeignKey(Store, related_name="product", on_delete=models.CASCADE)
    category = models.ForeignKey(
        Category, related_name="product", on_delete=models.CASCADE
    )

    title = models.CharField(max_length=80)
    desc = models.TextField(max_length=300, blank=True, null=True)

    is_active = models.BooleanField(default=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True, auto_now_add=False)
    slug = models.SlugField(blank=True, null=True)
    sold = models.IntegerField(_("terjual "), default=0)
    price = models.IntegerField(_("harga dalam Rupiah "), default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["penjual", "title"], name="you already have this title"
            )
        ]

        ordering = ["-create_at"]

    def __str__(self):
        return f"product {self.penjual} title {self.title}"

    @property
    def get_stock(self):
        qs = self.varian.filter(is_active=True)
        return sum(item.stock for item in qs)

    @property
    def get_rating_avg(self):
        return self.rating.all().aggregate(Avg("rating"))["rating__avg"]

    @property
    def get_price(self):
        return self.varian.all().aggregate(Min("price"))["price__min"]

    def get_rating(self):
        return self.rating.all()

    def get_thumb(self):
        return self.images.get(is_thumb=True)

    def get_image(self):
        return self.images.all()

    def get_varian(self):
        return self.varian.all()

    def get_order(self):
        varian = [item.get_order_item() for item in self.get_varian()]
        query = []
        for item in varian:
            
            query = [*list(item.values_list('id', flat=True)),*query]
            chain = [oItem.order.id for oItem in list(item)]
            query = [*chain,*query]         
        return query

class Rating(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="rating", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="rating", on_delete=models.CASCADE
    )
    rating = models.PositiveIntegerField(
        _(" rating"), validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    ulasan = models.TextField(_(" review"), max_length=300)
    create_at = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.product.title


class Bookmark(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name="bookmark", on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product, related_name="bookmark", on_delete=models.CASCADE
    )

    def __str__(self) -> str:

        return self.user.username + " bookmark "
