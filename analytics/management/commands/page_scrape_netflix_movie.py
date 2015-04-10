import datetime
from django.core.management import BaseCommand
from bs4 import BeautifulSoup
import requests
from analytics.models import *


class Command(BaseCommand):

    def handle(self, *args, **options):
        print page_scrape(args)

def page_scrape(args):

    for i in range(1978,6431):

        #Get IMDb ID from Viki Title
        netflix_qs = Netflix.objects.filter(id=i)
        print netflix_qs[0].title
        try:
            url="http://www.imdb.com/find?ref_=nv_sr_fn&q=" + str(netflix_qs[0].title) + " " + str(netflix_qs[0].release_year) + "&s=movies#tt"
            r = requests.get(url)
            soup = BeautifulSoup(r.content)
            results = soup.find("table", class_="findList")
            try:
                imdb_id = results.find("a")['href'][7:16]

                #Prep for Page Soup
                page_url = 'http://www.imdb.com/title/' + str(imdb_id)
                page_r = requests.get(page_url)
                page_soup = BeautifulSoup(page_r.content)

                #Grab Movie Data
                title = page_soup.find(itemprop="name").text
                print title
                try:
                    release_year = int(page_soup.find(itemprop="datePublished")['content'][:4])
                    release_month = int(page_soup.find(itemprop="datePublished")['content'][5:7])
                    release_day = int(page_soup.find(itemprop="datePublished")['content'][8:10])
                    release_date = datetime.date(release_year,release_month,release_day)
                except:
                    release_year = 2000
                    release_date = datetime.date(2000,01,01)
                print release_date
                try:
                    runtime_str = page_soup.find('time', itemprop="duration").text.strip()
                    runtime_list = [int(s) for s in runtime_str.split() if s.isdigit()]
                    runtime = int(runtime_list[0])
                except:
                    runtime = 0

                try:
                    mpaa_rating = page_soup.find(itemprop="contentRating")['content']
                except:
                    mpaa_rating = 'Null'
                try:
                    imdb_rating = page_soup.find('span',itemprop="ratingValue").text
                except:
                    imdb_rating = 0.0
                try:
                    if len(page_soup.find('p',itemprop="description").text.strip()) <= 200:
                        synopsis = page_soup.find('p',itemprop="description").text.strip()
                    elif len(page_soup.find('p',itemprop="description").text.strip()) > 200:
                        synopsis = page_soup.find('p',itemprop="description").text.strip()[0:199]
                except:
                    synopsis = 'Data Missing'
                imdb_url = page_url

                #Create Movie Data
                try:
                    content_qs = Content.objects.get_or_create(title=title,
                                           release_date=release_date,
                                           release_year=release_year,
                                           runtime=runtime,
                                           mpaa_rating=mpaa_rating,
                                           synopsis=synopsis,
                                           imdb_rating=imdb_rating,
                                           imdb_id=imdb_id,
                                           imdb_url=imdb_url,
                                           )
                    print content_qs

                    #Create/Grab ContentType
                    netflix_link_qs = Netflix.objects.get_or_create(id=i)
                    content_qs[0].netflix = netflix_link_qs[0]

                    #Create/Grab ContentType
                    name = 'movie'
                    content_type_qs = ContentType.objects.get_or_create(name=name)
                    content_qs[0].content_type = content_type_qs[0]

                    #Grab Genre Data
                    genres = []
                    for genre in page_soup.find_all('span', itemprop="genre"):
                        genre_temp = Genre.objects.get_or_create(name=genre.text)
                        genres.append(genre_temp[0])
                    #Connect Content to Genres
                    content_qs[0].genre.add(*genres)

                    #Grab Director Data
                    directors = []
                    for director in page_soup.find_all('div', itemprop="director"):
                        name = director.find('a').text
                        imdb_id = director.find('a')['href'][6:15]
                        imdb_url = 'http://www.imdb.com' + director.find('a')['href'][:16]

                        director_qs = Person.objects.get_or_create(name=name,
                                                                imdb_id=imdb_id,
                                                                imdb_url=imdb_url,
                                                                )

                        directors.append(director_qs[0])

                        #Create/Grab PersonType
                        person_type = []
                        name = 'director'
                        person_type_qs = PersonType.objects.get_or_create(name=name)
                        person_type.append(person_type_qs[0])
                        director_qs[0].type.add(*person_type)

                    #Connect Content to Director
                    content_qs[0].director.add(*directors)

                    #Grab Writer Data
                    writers = []
                    for writer in page_soup.find_all('div', itemprop="creator"):
                        name = writer.find('a').text
                        imdb_id = writer.find('a')['href'][6:15]
                        imdb_url = 'http://www.imdb.com' + writer.find('a')['href'][:16]
                        type = PersonType.objects.get_or_create(name="writer")

                        writer_qs = Person.objects.get_or_create(name=name,
                                                                imdb_id=imdb_id,
                                                                imdb_url=imdb_url,
                                                                )

                        writers.append(writer_qs[0])

                        #Create/Grab PersonType
                        person_type = []
                        name = 'writer'
                        person_type_qs = PersonType.objects.get_or_create(name=name)
                        person_type.append(person_type_qs[0])
                        writer_qs[0].type.add(*person_type)

                    #Connect Content to Director
                    content_qs[0].writer.add(*writers)

                    #Grab Actor/Character Data
                    for actor_even in page_soup.find_all('tr', 'even'):
                        if actor_even.find('td', itemprop="actor") != None:
                            #Create Actor
                            actor_name = actor_even.find('td', itemprop="actor").find('span').text
                            actor_imdb_id = actor_even.find('td', itemprop="actor").find('a')['href'][6:15]
                            actor_imdb_url = 'http://www.imdb.com' + actor_even.find('td', itemprop="actor").find('a')['href'][:16]

                            actor_qs = Person.objects.get_or_create(name=actor_name,
                                                                imdb_id=actor_imdb_id,
                                                                imdb_url=actor_imdb_url,
                                                                )

                            #Create/Grab PersonType
                            person_type = []
                            name = 'actor'
                            person_type_qs = PersonType.objects.get_or_create(name=name)
                            person_type.append(person_type_qs[0])
                            actor_qs[0].type.add(*person_type)

                            #Create Character
                            try:
                                character_type =[]
                                character_name = actor_even.find('td', class_="character").find('a').text
                                character_imdb_id = actor_even.find('td', class_="character").find('a')['href'][11:20]
                                character_imdb_url = 'http://www.imdb.com' + actor_even.find('td', class_="character").find('a')['href'][:21]
                                character_qs = Character.objects.get_or_create(name=character_name,
                                                                            imdb_id=character_imdb_id,
                                                                            imdb_url=character_imdb_url,
                                                                            )
                                character_type.append(character_qs[0])
                                #Connect to Actor
                                actor_type = []
                                actor_type.append(actor_qs[0])
                                character_qs[0].actor.add(*actor_type)
                                content_qs[0].characters.add(*character_type)



                            except AttributeError:
                                pass
                        else:
                            pass
                    for actor_odd in page_soup.find_all('tr', 'odd'):
                        if actor_odd.find('td', itemprop="actor") != None:
                            #Creator Actor
                            actor_name = actor_odd.find('td', itemprop="actor").find('span').text
                            actor_imdb_id = actor_odd.find('td', itemprop="actor").find('a')['href'][6:15]
                            actor_imdb_url = 'http://www.imdb.com' + actor_odd.find('td', itemprop="actor").find('a')['href'][:16]

                            actor_qs = Person.objects.get_or_create(name=actor_name,
                                                                imdb_id=actor_imdb_id,
                                                                imdb_url=actor_imdb_url,
                                                                )

                            #Create/Grab PersonType
                            person_type = []
                            name = 'actor'
                            person_type_qs = PersonType.objects.get_or_create(name=name)
                            person_type.append(person_type_qs[0])
                            actor_qs[0].type.add(*person_type)

                            #Create Character
                            try:
                                character_type =[]
                                character_name = actor_odd.find('td', class_="character").find('a').text
                                character_imdb_id = actor_odd.find('td', class_="character").find('a')['href'][11:20]
                                character_imdb_url = 'http://www.imdb.com' + actor_odd.find('td', class_="character").find('a')['href'][:21]
                                character_qs = Character.objects.get_or_create(name=character_name,
                                                                            imdb_id=character_imdb_id,
                                                                            imdb_url=character_imdb_url,
                                                                            )

                                character_type.append(character_qs[0])
                                #Connect to Actor
                                actor_type = []
                                actor_type.append(actor_qs[0])
                                character_qs[0].actor.add(*actor_type)
                                content_qs[0].characters.add(*character_type)

                            except AttributeError:
                                pass
                        else:
                            pass

                    print content_qs[0].title + ' = Done!'
                    content_qs[0].save()
                except:
                    pass
            except AttributeError:
                pass
        except UnicodeEncodeError:
            pass