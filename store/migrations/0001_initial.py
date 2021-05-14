# Generated by Django 3.2 on 2021-05-14 16:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('costumer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=70)),
                ('slug', models.SlugField(blank=True, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=80)),
                ('desc', models.TextField(blank=True, max_length=300, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(blank=True, null=True)),
                ('sold', models.IntegerField(default=0, verbose_name='terjual ')),
                ('price', models.IntegerField(default=0, verbose_name='harga dalam Rupiah ')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store.category')),
                ('penjual', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product', to='costumer.store')),
            ],
            options={
                'ordering': ['-create_at'],
            },
        ),
        migrations.CreateModel(
            name='Varian',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('stock', models.PositiveIntegerField(default=0)),
                ('is_active', models.BooleanField(default=True)),
                ('price', models.IntegerField(validators=[django.core.validators.MaxValueValidator(99999999), django.core.validators.MinValueValidator(0)], verbose_name=' price in IDR')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='varian', to='store.product')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)], verbose_name=' rating')),
                ('ulasan', models.TextField(max_length=200, verbose_name=' review')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(height_field='height_field', upload_to='product', width_field='width_field')),
                ('height_field', models.PositiveIntegerField(default=0)),
                ('width_field', models.PositiveIntegerField(default=0)),
                ('is_thumb', models.BooleanField(default=False)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to='store.product')),
                ('varian', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image_varian', to='store.varian')),
            ],
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark', to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmark', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='product',
            constraint=models.UniqueConstraint(fields=('penjual', 'title'), name='you already have this title'),
        ),
    ]
