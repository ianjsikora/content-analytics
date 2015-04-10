from django.core.management import BaseCommand
from local_settings import IMPORT_IO_KEY
from analytics.models import IMDb
import requests
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        print get_content(args)

def get_content(args):

    base_url = "https://api.import.io/store/data/eaacd733-7fad-4149-a29c-2fc015fb6c8b/_query?input/webpage/url=http%3A%2F%2Fwww.imdb.com%2Ffeatures%2Fvideo%2Fbrowse%2Ffilm%2F&_user=3a3a8670-4c8c-4592-b467-789ceac08c24&_apikey="
    url = base_url + IMPORT_IO_KEY
    request = requests.get(url)
    results = request.json()["results"]
    for i in range(len(results)):
        titletemp = results[i]["link/_text"]
        if titletemp.index(")") == len(titletemp) - 1 and titletemp.index(")") - titletemp.index("(") > 4:
            title = titletemp[0:titletemp.index(")") - 6]
            release_year = int(titletemp[titletemp.index(")")-4 : titletemp.index(")")])
        else:
            title = titletemp
            release_year = None
        print title
        print release_year
        imdb_streaming_url = results[i]["link"]
        print imdb_streaming_url
        imdb_id = results[i]["link/_source"][7:]
        print imdb_id
        imdb_write = IMDb.objects.get_or_create (
            title=title,
            type="movie",
            release_year=release_year,
            imdb_streaming_url=imdb_streaming_url,
            imdb_id=imdb_id,
        )
        print imdb_write