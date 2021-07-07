# Generated by Django 3.2 on 2021-07-03 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('store', '0002_auto_20210627_1910'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notifikasi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('type_notif', models.PositiveIntegerField(choices=[(1, 'Order'), (2, 'Massage')])),
                ('more_text', models.TextField(blank=True, null=True)),
                ('is_seen', models.BooleanField(default=False)),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='product', to='store.product')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='penerima', related_query_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', related_query_name='pengirim', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-create_at'],
            },
        ),
    ]