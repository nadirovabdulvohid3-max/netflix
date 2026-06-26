from django.db import models
from Actor.models import Actor
from django.contrib.auth.models import User

class Movie(models.Model):
    name = models.CharField(max_length=255)
    year = models.IntegerField()
    imdb = models.FloatField()
    genre = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor, related_name='movies')

class Comment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"