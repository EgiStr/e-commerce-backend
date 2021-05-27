# Generated by Django 3.2 on 2021-05-24 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('costumer', '0002_tokennotif'),
        ('order', '0002_alter_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='order', to='costumer.store'),
            preserve_default=False,
        ),
    ]