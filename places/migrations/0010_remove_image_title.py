# Generated by Django 4.1.2 on 2022-10-24 15:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0009_image_delete_placeimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='title',
        ),
    ]
