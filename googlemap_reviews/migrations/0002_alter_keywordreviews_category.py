# Generated by Django 5.0.2 on 2024-05-08 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('googlemap_reviews', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keywordreviews',
            name='category',
            field=models.BooleanField(choices=[(1, '好評'), (2, '負評')], verbose_name='類別'),
        ),
    ]
