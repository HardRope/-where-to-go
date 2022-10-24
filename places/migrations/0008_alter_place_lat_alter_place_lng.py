# Generated by Django 4.1.2 on 2022-10-24 15:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0007_alter_place_description_long_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='place',
            name='lat',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=22, verbose_name='Широта'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='place',
            name='lng',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=22, verbose_name='Долгота'),
            preserve_default=False,
        ),
    ]