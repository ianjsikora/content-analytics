import urllib
from django.core.management import BaseCommand
from analytics.models import Viki
from bs4 import BeautifulSoup
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        print get_content(args)

def get_content(args):

    json_data = open('analytics/management/commands/data/viki_streaming_movie.json')
    list = json_data
    data2 = json.load(list)
    print len(data2['results']['collection1'])

    for i in range(0,len(data2['results']['collection1'])):
        title = data2['results']['collection1'][i]['title']['text']
        link = data2['results']['collection1'][i]['title']['href']
        country = data2['results']['collection1'][i]['country']
        print title
        print link
        print country
        viki_write = Viki.objects.get_or_create (
            title=title,
            type='movie',
            country=country,
            viki_url=link,
        )
        print viki_write
    json_data.close()