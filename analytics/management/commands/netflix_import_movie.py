from django.core.management import BaseCommand
from analytics.models import Netflix
import json

class Command(BaseCommand):

    def handle(self, *args, **options):
        print get_content(args)

def get_content(args):

    json_data = open('analytics/management/commands/data/netflix_movies.json')
    list = json_data
    data2 = json.load(list)
    print len(data2['data'])

    for i in range(0,len(data2['data'])):
        title = data2['data'][i]['title'][0]
        print "Title: " + title
        string = data2['data'][i]['year_runtime_rating'][0]
        print string
        if "Rating:" in string:
            rating = float(string[string.index(":") + 2:string.index(".") + 2])
        else:
            rating = None
        print "Rating: " + str(rating)
        if "-" in string:
            year = int(string[string.index("-") - 5:string.index("-") - 1])
        else:
            year = None
        print "Year: " + str(year)
        url_length = len(data2['data'][i]['netflix_url'][0])
        url = data2['data'][i]['netflix_url'][0][11:url_length]
        netflix_url =  "http://www.netflix.com" + url
        print "Netflix_URL: " + str(netflix_url)
        netflix_write = Netflix.objects.get_or_create (
            title=title,
            type='movie',
            release_year=year,
            netflix_rating=rating,
            netflix_url=netflix_url,
        )
        print netflix_write
    json_data.close()