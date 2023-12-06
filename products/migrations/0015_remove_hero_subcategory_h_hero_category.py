# Generated by Django 4.2.7 on 2023-12-04 09:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_hero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hero',
            name='subcategory_h',
        ),
        migrations.AddField(
            model_name='hero',
            name='category',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.category'),
            preserve_default=False,
        ),
    ]
