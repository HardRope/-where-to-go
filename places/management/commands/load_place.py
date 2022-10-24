import logging
import requests

from places.models import Place, Image

from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile


def add_imgs_to_place(place, num, url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        place_image, created = Image.objects.get_or_create(
            place=place,
            position=num,
        )

        place_image.image.save(
            f'{num} {place}',
            ContentFile(response.content),
            save=True
        )
    except requests.HTTPError:
        logging.info('Не удалось загрузить изображение')
    except MultipleObjectsReturned:
        logging.info('Существует больше одного места с таким названием')


def add_place(serialized_place):
    title = serialized_place['title']
    description_short = serialized_place['description_short']
    description_long = serialized_place['description_long']
    lng = serialized_place['coordinates']['lng']
    lat = serialized_place['coordinates']['lat']

    images_urls = serialized_place['imgs']

    place, created = Place.objects.get_or_create(
        title=title,
        description_short=description_short,
        description_long=description_long,
        lng=lng,
        lat=lat,
    )

    for num, url in enumerate(images_urls, start=1):
        add_imgs_to_place(place, num, url)


def main(url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        serialized_place = response.json()

        add_place(serialized_place)
    except requests.HTTPError:
        logging.info('Ошибка загрузки. Проверьте ссылку')


class Command(BaseCommand):
    help = 'Loading place to db from url with json'

    def handle(self, *args, **options):
        main(options['url'])

    def add_arguments(self, parser):
        parser.add_argument('url')
