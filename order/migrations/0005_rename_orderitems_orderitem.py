# Generated by Django 4.0.6 on 2022-07-12 08:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0001_initial'),
        ('order', '0004_alter_order_status_orderitems'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='OrderItems',
            new_name='OrderItem',
        ),
    ]
