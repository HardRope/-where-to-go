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

        Image.objects.get_or_create(
            place=place,
            position=num,
            image=ContentFile(response.content, name=f'{num} {place}')
        )
    except requests.HTTPError:
        logging.info('Не удалось загрузить изображение')
    except MultipleObjectsReturned:
        logging.info('Существует больше одного места с таким названием')


def add_place(serialized_place):
    try:
        title = serialized_place['title']

        place_descriptions = {
            'description_short': serialized_place.get('description_short', ''),
            'description_long': serialized_place.get('description_long', ''),
            'lng': serialized_place['coordinates']['lng'],
            'lat': serialized_place['coordinates']['lat'],
            'images': serialized_place.get('imgs', []),
        }
    except KeyError:
        logging.info(f'Не хватает обязательного аргумента {KeyError}')
        return

    images_urls = place_descriptions['images']

    place, created = Place.objects.update_or_create(
        title=title,
        defaults=place_descriptions
    )
    if not created:
        return

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
