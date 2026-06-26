from rest_framework import serializers
from .models import Movie, Comment
from Actor.serializers import ActorSerializer

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'movie', 'text', 'created_date']
        read_only_fields = ['id', 'created_date']

class MovieDetailSerializer(serializers.ModelSerializer):
    actors = ActorSerializer(many=True, read_only=True)
    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'imdb', 'genre', 'actors']

class MovieWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ['id', 'name', 'year', 'imdb', 'genre', 'actors']