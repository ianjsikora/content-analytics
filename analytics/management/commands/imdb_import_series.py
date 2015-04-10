from django.core.management import BaseCommand
from local_settings import IMPORT_IO_KEY
from analytics.models import IMDb
import requests
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        print get_content(args)

def get_content(args):

    base_url = "https://api.import.io/store/data/9f0b0575-d4e0-4eef-8135-5f656789052d/_query?input/webpage/url=http%3A%2F%2Fwww.imdb.com%2Ffeatures%2Fvideo%2Fbrowse%2Ftv%2F&_user=3a3a8670-4c8c-4592-b467-789ceac08c24&_apikey="
    url = base_url + IMPORT_IO_KEY
    request = requests.get(url)
    results = request.json()['results']
    for i in range(len(results)):
        titletemp = results[i]['link_1/_text']
        if titletemp.index("(") > 0:
            title = titletemp[0:titletemp.index("(") - 1]
        else:
            title = titletemp
        print title
        if titletemp.index("(") > 0:
            release_year = int(titletemp[titletemp.index("(")+1:titletemp.index("(")+5])
        else:
            release_year = int(results[i]['link_1_numbers'])
        print release_year
        episodes = int(results[i]['link_2/_text'])
        print episodes
        imdb_streaming_url = results[i]["link_2"]
        print imdb_streaming_url
        imdb_id = results[i]["link_1/_source"][7:]
        print imdb_id
        imdb_write = IMDb.objects.get_or_create (
            title=title,
            type='series',
            release_year=release_year,
            episodes=episodes,
            imdb_streaming_url=imdb_streaming_url,
            imdb_id=imdb_id,
        )
        print imdb_write