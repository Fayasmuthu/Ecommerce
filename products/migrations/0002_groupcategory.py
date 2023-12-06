# Generated by Django 4.2.7 on 2023-11-25 06:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groupcategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.SlugField(max_length=100)),
            ],
            options={
                'verbose_name': 'Group Category',
                'verbose_name_plural': 'Group Categories',
                'ordering': ('id',),
            },
        ),
    ]