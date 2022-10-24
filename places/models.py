from django.db import models
from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField(
        'Название',
        max_length=200,
        unique=True,
    )

    description_short = models.TextField(
        'Краткое описание',
        blank=True,
    )

    description_long = HTMLField(
        'Полное описание',
        blank=True,
    )

    lng = models.DecimalField(
        'Долгота',
        max_digits=22,
        decimal_places=16,
    )

    lat = models.DecimalField(
        'Широта',
        max_digits=22,
        decimal_places=16,
    )

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'

    def __str__(self):
        return self.title


class Image(models.Model):
    place = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE,
        related_name='images',
    )

    image = models.ImageField()

    position = models.IntegerField(
        default=1,
        db_index=True
    )

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
        ordering = ('position',)

    def __str__(self):
        return f'{self.position} {self.place.title}'
