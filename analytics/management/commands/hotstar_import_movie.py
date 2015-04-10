from bs4 import BeautifulSoup
from django.core.management import BaseCommand
import requests


class Command(BaseCommand):

    def handle(self, *args, **options):
        print page_scrape(args)

def page_scrape(args):

    url = "http://www.hotstar.com/#!/watch-movies-online"
    r = requests.get(url)
    soup = BeautifulSoup(r.content)
    print soup
