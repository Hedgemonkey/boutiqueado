# Generated by Django 5.1.4 on 2025-01-23 02:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bag', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderlineitem',
            name='order',
        ),
        migrations.RemoveField(
            model_name='orderlineitem',
            name='product',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderLineItem',
        ),
    ]
