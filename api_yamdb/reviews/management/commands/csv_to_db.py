import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

Models = {
    User: 'users.csv',
    Category: 'category.csv',
    Title: 'titles.csv',
    Genre: 'genre.csv',
    Review: 'review.csv',
    Comment: 'comments.csv',
    # Title.genre.through: 'genre_title.csv',
}


class Command(BaseCommand):
    help = 'Can load csv-files to DB'

    def handle(self, *args, **options):

        for model, csv_files in Models.items():
            with open(
                f'{settings.STATICFILES_DIRS}/data/{csv_files}',
                'r',
                encoding='utf-8'
            ) as csv_file:
                reader = csv.DictReader(csv_file)
                model.objects.bulk_create(
                    model(**data) for data in reader
                )
            self.stdout.write(
                f'Data for {model.__name__} uploaded')
        return('Data uploaded successfully')
