import requests
import datetime
from django.core.management import BaseCommand
from analytics.models import Content
from analytics.models import Genre
from analytics.models import Character
from analytics.models import Person
from local_settings import SECRET_KEY_API

class Command(BaseCommand):

    def handle(self, *args, **options):
        print get_content(args)

def get_content(args):

    #Check if content is already in the database
    for i in range(len(args)):
        imdb_target = args[i]

        #Define API Links
        imdb_url = "http://www.omdbapi.com/?i=" + imdb_target + "&plot=full&r=json"
        print imdb_url
        imdb = requests.get(imdb_url)
        print imdb
        tomato_target = imdb.json()['Title']
        tomato_url = "http://api.rottentomatoes.com/api/public/v1.0/movies.json?apikey=" + SECRET_KEY_API + tomato_target + "&page_limit=1"

        tomato = requests.get(tomato_url)
        print tomato.json()

        #Grab Movie Data
        title = imdb.json()['Title']
        kind = imdb.json()['Type']
        date_list = imdb.json()['Released'].split()
        date_dict = dict([('Jan',1),('Feb',2),('Mar',3),('Apr',4),('May',5),('Jun',6),('Jul',7),('Aug',8),('Sep',9),('Oct',10),('Nov',11),('Dec',12)])
        date_list[0] = int(date_list[0])
        date_list[1] = int(date_dict[date_list[1]])
        date_list[2] = int(date_list[2])
        release_date = datetime.date(date_list[2], date_list[1], date_list [0])
        runtime_list = imdb.json()['Runtime'].split()
        runtime = int(runtime_list[0])
        rating = imdb.json()['Rated']
        synopsis = imdb.json()['Plot']
        if tomato.json()['movies'][0]['ratings']['critics_score']:
            rating_tomato_c = tomato.json()['movies'][0]['ratings']['critics_score']
        if tomato.json()['movies'][0]['ratings']['audience_score']:
            rating_tomato_a = tomato.json()['movies'][0]['ratings']['audience_score']
        rating_imdb = float(imdb.json()['imdbRating'])
        if tomato.json()['movies'][0]['posters']['original']:
            poster = tomato.json()['movies'][0]['posters']['original'].replace('_tmb', '_lgr')
        if tomato.json()['movies'][0]['id']:
            tomato_id = tomato.json()['movies'][0]['id']
        IMDb_id = imdb.json()['imdbID']
        IMDB_url = 'http://www.imdb.com/title/' + imdb_target

        #Create Movie
        content_qs = Content.objects.get_or_create(title=title,
                               type=kind,
                               release_date=release_date,
                               runtime=runtime,
                               rating=rating,
                               synopsis=synopsis,
                               rating_tomato_c=rating_tomato_c,
                               rating_tomato_a=rating_tomato_a,
                               rating_imdb=rating_imdb,
                               poster=poster,
                               tomato_id=tomato_id,
                               IMDb_id=IMDb_id,
                               IMDB_url=IMDB_url,
                               )

        #Get Genres Data
        genres_url = tomato.json()['movies'][0]['links']['self'] + "?apikey=" + SECRET_KEY_API + tomato_target + "&page_limit=1"
        genre_request = requests.get(genres_url)
        genre = genre_request.json()['genres']
        genres = []
        for j in range(len(genre)):
            Genre.objects.get_or_create(name=genre[j])
            genres.extend(Genre.objects.filter(name=genre[j]))

        #Link Content to Genres
        content_qs[0].genre.add(*genres)

        #Get Character Data
        character_url = tomato.json()['movies'][0]['links']['cast'] + "?apikey=" + SECRET_KEY_API + tomato_target + "&page_limit=1"
        character_request = requests.get(character_url)
        character = character_request.json()['cast']
        characters = []
        for j in range(len(character)):
            for k in range(len(character[j]['characters'])):
                character_qs = Character.objects.get_or_create(name=character[j]['characters'][k],
                                                               tomato_id=character[j]['id'])
                characters.extend(Character.objects.filter(name=character[j]['characters'][k]))
                actor_qs = Person.objects.get_or_create(name=character[j]['name'],
                                                        type='actor',
                                                        tomato_id=character[j]['id'])
                actor_qs[0].roles.add(character_qs[0])

        # Link Content to Characters
        content_qs[0].cast.add(*characters)