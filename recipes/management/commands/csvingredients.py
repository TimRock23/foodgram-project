import csv
import os
import sqlite3

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Import ingredients.csv to DB table recipes_ingredient'

    def handle(self, *args, **options):
        base_dir = os.getcwd()
        csv_file = os.path.join(base_dir, 'data/ingredients.csv')

        conn = sqlite3.connect('db.sqlite3')
        cur = conn.cursor()

        with open(csv_file, 'r') as fin:
            dr = csv.DictReader(fin)
            to_db = [
                (i['title'], i['dimension'])
                for i in dr
            ]

        cur.executemany(
            '''INSERT INTO recipes_ingredient (title, dimension)
            VALUES (?, ?);''',
            to_db
        )
        conn.commit()
        conn.close()
