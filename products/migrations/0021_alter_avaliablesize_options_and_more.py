# Generated by Django 4.2.7 on 2023-12-19 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0020_gallery_preview'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='avaliablesize',
            options={'ordering': ('discount',), 'verbose_name': 'Available Size', 'verbose_name_plural': 'Available Sizes'},
        ),
        migrations.RenameField(
            model_name='avaliablesize',
            old_name='price',
            new_name='discount',
        ),
    ]
