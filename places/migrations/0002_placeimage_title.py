# Generated by Django 3.2.15 on 2022-10-04 21:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='placeimage',
            name='title',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Название'),
        ),
    ]
