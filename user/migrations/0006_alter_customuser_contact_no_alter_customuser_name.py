# Generated by Django 4.2.11 on 2024-04-10 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_alter_customuser_contact_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='contact_no',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]