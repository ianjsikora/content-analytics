from django.core.management import BaseCommand
from analytics.models import Amazon
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        print get_content(args)

def get_content(args):

    json_data = open('analytics/management/commands/data/amazon_prime_movies.json')
    list = json_data
    data2 = json.load(list)

    for i in range(0,len(data2['data'])):
        title = data2['data'][i]['title'][0]
        print "Title: " + title
        string = data2['data'][i]['year_mpaa_runtime'][0]
        print string
        if string.index("-") == 5:
            year = int(string[0:4])
        else:
            year = None
        print "Year: " + str(year)
        url = data2['data'][i]['streaming_link'][0]
        print "Amazon_URL: " + str(url)
        amazon_write = Amazon.objects.get_or_create (
            title=title,
            type='movie',
            release_year=year,
            amazon_url=url,
        )
        print amazon_write
    json_data.close()