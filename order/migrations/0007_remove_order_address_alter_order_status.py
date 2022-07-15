# Generated by Django 4.0.6 on 2022-07-12 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0006_order_address_alter_order_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(blank=True, choices=[('Success', 'Success'), ('Failed', 'Failed')], max_length=7, null=True),
        ),
    ]