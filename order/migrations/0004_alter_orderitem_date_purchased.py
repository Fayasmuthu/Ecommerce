# Generated by Django 4.2.7 on 2023-12-05 11:53

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_orderitem_date_purchased_orderitem_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='date_purchased',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
