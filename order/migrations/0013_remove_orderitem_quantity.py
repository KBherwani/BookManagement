# Generated by Django 4.0.6 on 2022-07-12 11:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0012_remove_orderitem_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderitem',
            name='quantity',
        ),
    ]
