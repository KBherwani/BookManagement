# Generated by Django 4.0.6 on 2022-07-12 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0016_alter_order_order_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_id',
            field=models.CharField(default=1, max_length=12),
        ),
    ]
