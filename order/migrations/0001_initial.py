# Generated by Django 4.2.7 on 2023-12-04 06:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_Name', models.CharField(max_length=50)),
                ('last_Name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.IntegerField()),
                ('company', models.CharField(blank=True, max_length=200, null=True)),
                ('country', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('postcode', models.IntegerField()),
                ('address', models.TextField()),
                ('address1', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store', models.CharField(max_length=50)),
                ('image', models.ImageField(upload_to='media/order_image')),
                ('quantity', models.IntegerField()),
                ('price', models.FloatField()),
                ('total', models.IntegerField()),
                ('paid', models.BooleanField(default=False)),
                ('orders', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orders')),
            ],
        ),
    ]
