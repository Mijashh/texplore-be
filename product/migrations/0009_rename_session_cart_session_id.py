# Generated by Django 4.2.11 on 2024-04-19 10:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0008_cart_session'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='session',
            new_name='session_id',
        ),
    ]