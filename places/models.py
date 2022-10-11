from django.db import models

class Place(models.Model):
    title = models.CharField(
        'Название',
        max_length=200,
    )

    description_short = models.TextField(
        'Краткое описание',
        blank=True,
        null=True,
    )

    description_long = models.TextField(
        'Полное описание',
        blank=True,
        null=True,

    )

    lng = models.DecimalField(
        'Долгота',
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
    )

    lat = models.DecimalField(
        'Широта',
        max_digits=22,
        decimal_places=16,
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'место'
        verbose_name_plural = 'места'


class PlaceImage(models.Model):
    place = models.ForeignKey(
        'Place',
        on_delete=models.CASCADE,
        related_name='images',
    )

    title = models.CharField(
        'Название',
        max_length=200,
        blank=True,
        null=True,
    )

    image = models.ImageField(
        blank=True,
        null=True,
    )

    position = models.IntegerField(
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
        unique_together = ['place', 'position',]

