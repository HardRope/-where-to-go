import logging
import requests

from places.models import Place, Image

from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile


def load_place_image(place, num, url):
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
    title = serialized_place.get('title')

    place_descriptions = {
        'description_short': serialized_place.get('description_short', ''),
        'description_long': serialized_place.get('description_long', ''),
        'lng': serialized_place.get('coordinates').get('lng'),
        'lat': serialized_place.get('coordinates').get('lat'),
    }

    if not title:
        logging.info('Требуется указать название места')
        return
    elif not place_descriptions['lng']:
        logging.info('Требуется указать координаты долготы (lng)')
        return
    elif not place_descriptions['lat']:
        logging.info('Требуется указать координаты широты (lat)')
        return

    images_urls = serialized_place['imgs']

    place, created = Place.objects.update_or_create(
        title=title,
        defaults=place_descriptions
    )

    for num, url in enumerate(images_urls, start=1):
        load_place_image(place, num, url)


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
