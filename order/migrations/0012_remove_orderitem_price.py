# Generated by Django 4.0.6 on 2022-07-12 11:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0011_remove_orderitem_items_orderitem_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
    ]