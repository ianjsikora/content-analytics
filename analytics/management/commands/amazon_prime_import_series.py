from django.core.management import BaseCommand
from analytics.models import Amazon
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        print get_content(args)

def get_content(args):

    json_data = open('analytics/management/commands/data/amazon_prime_series.json')
    list = json_data
    data2 = json.load(list)

    print len(data2['tiles'][0]['results'][0]['pages'])
    print len(data2['tiles'][0]['results'][0]['pages'][0]['results'])

    for i in range(0,284):
        for j in range(0,10):
            title = data2['tiles'][0]['results'][0]['pages'][i]['results'][j]['title']
            print "Title: " + title
            string = data2['tiles'][0]['results'][0]['pages'][0]['results'][j]['year_mpaa_runtime']
            print string
            if string.index("-") == 5:
                year = int(string[0:4])
            else:
                year = None
            print "Year: " + str(year)
            url = data2['tiles'][0]['results'][0]['pages'][0]['results'][j]['prime_url']
            print "Amazon_URL: " + str(url)
            amazon_write = Amazon.objects.get_or_create (
                title=title,
                type='series',
                release_year=year,
                amazon_url=url,
            )
            print amazon_write
        json_data.close()