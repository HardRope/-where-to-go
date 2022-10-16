import argparse
import logging
import requests

from places.models import Place, PlaceImage

from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile


def add_imgs_to_place(place, num, url):
    try:
        response = requests.get(url)
        response.raise_for_status()

        image_title = f'{num} {place.title}'
        place_image, created = PlaceImage.objects.get_or_create(
            place=place,
            title=image_title,
            position=num,
        )

        place_image.image.save(f'{image_title}.jpg', ContentFile(response.content), save=True)
    except requests.HTTPError:
        logging.info('Не удалось загрузить изображение')
    except MultipleObjectsReturned:
        logging.info('Существует больше одного места с таким названием')


def add_place(json):
    title = json['title']
    description_short = json['description_short']
    description_long = json['description_long']
    lng = json['coordinates']['lng']
    lat = json['coordinates']['lat']

    images_urls = json['imgs']

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

        place_json = response.json()

        add_place(place_json)
    except requests.HTTPError:
        logging.info('Ошиибка загрузки. Проверьте ссылку')


class Command(BaseCommand):
    help = 'Loading place to db from url with json'

    def handle(self, *args, **options):
        main(options['url'])

    def add_arguments(self, parser):
        parser.add_argument('url')