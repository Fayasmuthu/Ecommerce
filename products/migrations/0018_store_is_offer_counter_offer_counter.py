# Generated by Django 4.2.7 on 2023-12-06 10:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0017_remove_category_image_hero_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='store',
            name='is_offer_counter',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='offer_counter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_hero', models.ImageField(blank=True, null=True, upload_to='img/hero')),
                ('title_with', models.CharField(blank=True, max_length=150, null=True)),
                ('topic_hero', models.CharField(blank=True, max_length=200, null=True)),
                ('with_title', models.CharField(blank=True, max_length=200, null=True)),
                ('sale_end_date', models.DateField(blank=True, null=True)),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.store')),
            ],
        ),
    ]