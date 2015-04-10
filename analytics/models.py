from django.db import models

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

class Keyword(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

class ContentType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

class SourceType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

class PersonType(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return unicode(self.name)

class Person(models.Model):
    name = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=30, null=True)
    imdb_url = models.URLField(null=True)
    headshot = models.URLField(null=True)
    # Connections to other tables
    type = models.ManyToManyField(PersonType)

    def __unicode__(self):
        return self.name

class Character(models.Model):
    name = models.CharField(max_length=100)
    imdb_id = models.CharField(max_length=30, null=True)
    imdb_url = models.URLField(null=True)

    # Connections to other tables
    actor = models.ManyToManyField(Person)

    def __unicode__(self):
        return unicode(self.name)

class Amazon(models.Model):
    title = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('movie', 'Movie'),
        ('series', 'Series'),
    )
    type = models.CharField(max_length=6,
                            choices=TYPE_CHOICES,
                            default='movie')
    season = models.IntegerField(null=True)
    release_year = models.IntegerField(null=True)
    amazon_rating = models.IntegerField(null=True)
    amazon_url = models.URLField(null=True)
    imdb_id = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.title

class Netflix(models.Model):
    title = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('movie', 'Movie'),
        ('series', 'Series'),
    )
    type = models.CharField(max_length=6,
                            choices=TYPE_CHOICES,
                            default='movie')
    season = models.IntegerField(null=True)
    release_year = models.IntegerField(null=True)
    netflix_rating = models.IntegerField(null=True)
    netflix_url = models.URLField(null=True)

    def __unicode__(self):
        return self.title

class IMDb(models.Model):
    title = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('movie', 'Movie'),
        ('series', 'Series'),
    )
    type = models.CharField(max_length=6,
                            choices=TYPE_CHOICES,
                            default='movie')
    release_year = models.IntegerField(null=True)
    episodes = models.IntegerField(null=True)
    imdb_streaming_url = models.URLField(null=True)
    imdb_id = models.CharField(max_length=30, null=True)

    def __unicode__(self):
        return self.title
        return self.release_year

class Viki(models.Model):
    title = models.CharField(max_length=100)
    TYPE_CHOICES = (
        ('movie', 'Movie'),
        ('series', 'Series'),
    )
    type = models.CharField(max_length=6,
                            choices=TYPE_CHOICES,
                            default='movie')
    country = models.CharField(max_length=50, null=True)
    viki_url = models.URLField(null=True)

    def __unicode__(self):
        return self.title

class Content(models.Model):
    # Movie Metadata
    title = models.CharField(max_length=100)
    release_date = models.DateField(null=True)
    release_year = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)
    mpaa_rating = models.CharField(max_length=10)
    budget = models.IntegerField(null=True)
    revenue = models.IntegerField(null=True)
    synopsis = models.TextField(null=True)
    imdb_rating = models.FloatField(null=True)
    poster = models.URLField(null=True)
    imdb_id = models.CharField(max_length=30, null=True)
    imdb_url = models.URLField(null=True)

    # Sources
    netflix= models.ForeignKey(Netflix, null=True)
    # imdb= models.ForeignKey(IMDb, null=True)
    # hulu = models.ForeignKey(null=True)
    amazon = models.ForeignKey(Amazon, null=True)
    viki = models.ForeignKey(Viki, null=True)

    genre = models.ManyToManyField(Genre)
    director = models.ManyToManyField(Person,related_name="director")
    writer = models.ManyToManyField(Person,related_name="writer")
    characters = models.ManyToManyField(Character)
    content_type = models.ForeignKey(ContentType, null=True)
    source_types = models.ManyToManyField(SourceType)
    keywords = models.ManyToManyField(Keyword)

    def __unicode__(self):
        return unicode(self.title)