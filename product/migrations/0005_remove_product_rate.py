# Generated by Django 4.2.11 on 2024-04-17 08:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_alter_product_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='rate',
        ),
    ]