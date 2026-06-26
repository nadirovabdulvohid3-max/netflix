from Actor.models import Actor
from Movie.serializers import MovieDetailSerializer
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from Movie.models import Movie

class MovieViewSetListTestCase(APITestCase):
    def setUp(self):
        self.actor1 = Actor.objects.create(name="Leonardo DiCaprio")
        self.actor2 = Actor.objects.create(name="Matthew McConaughey")
        self.movie1 = Movie.objects.create(
            name="Inception",
            year=2010,
            imdb=8.8,
            genre="Sci-Fi")
        self.movie1.actors.add(self.actor1)

        self.movie2 = Movie.objects.create(
            name="Interstellar",
            year=2014,
            imdb=8.7,
            genre="Sci-Fi")
        self.movie2.actors.add(self.actor2)

        self.movie3 = Movie.objects.create(
            name="The Dark Knight",
            year=2008,
            imdb=9.0,
            genre="Action"
)
        self.url = reverse('movie-list')

    def test_get_all_movies_success(self):
        response = self.client.get(self.url)
        movies = Movie.objects.all().order_by('-imdb')
        serializer = MovieDetailSerializer(movies, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        self.assertEqual(response.data, serializer.data)

    def test_movie_list_search_by_name(self):
        response = self.client.get(self.url, {'search': 'Inception'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Inception")

    def test_movie_list_search_by_genre(self):
        response = self.client.get(self.url, {'search': 'Sci-Fi'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_movie_list_ordering_by_imdb(self):
        response = self.client.get(self.url, {'ordering': 'imdb'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['imdb'], 8.7)
        self.assertEqual(response.data[-1]['imdb'], 9.0)


class MovieSearchTestCase(APITestCase):
    def setUp(self):
        Movie.objects.create(name="Avatar", year=2009, imdb=7.9, genre="Sci-Fi")
        Movie.objects.create(name="The Avengers", year=2012, imdb=8.0, genre="Action")
        Movie.objects.create(name="Gladiator", year=2000, imdb=8.5, genre="Action")
        self.url = reverse('movie-list')

    def test_search_by_exact_name(self):
        response = self.client.get(self.url, {'search': 'Avatar'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Avatar")

    def test_search_by_partial_name(self):
        response = self.client.get(self.url, {'search': 'Av'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_by_genre(self):
        response = self.client.get(self.url, {'search': 'Action'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_case_insensitivity(self):
        response = self.client.get(self.url, {'search': 'action'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_no_results(self):
        response = self.client.get(self.url, {'search': 'Titanic'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)





class MovieOrderingTestCase(APITestCase):
    def setUp(self):
        Movie.objects.create(name="Gladiator", year=2000, imdb=8.5, genre="Action")
        Movie.objects.create(name="The Shawshank Redemption", year=1994, imdb=9.2, genre="Drama")
        Movie.objects.create(name="The Matrix", year=1999, imdb=7.8, genre="Sci-Fi")
        self.url = reverse('movie-list')

    def test_default_ordering_by_imdb_descending(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['imdb'], 9.2)
        self.assertEqual(response.data[1]['imdb'], 8.5)
        self.assertEqual(response.data[2]['imdb'], 7.8)

    def test_explicit_ordering_by_imdb_ascending(self):
        response = self.client.get(self.url, {'ordering': 'imdb'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['imdb'], 7.8)
        self.assertEqual(response.data[1]['imdb'], 8.5)
        self.assertEqual(response.data[2]['imdb'], 9.2)

    def test_explicit_ordering_by_imdb_descending(self):
        response = self.client.get(self.url, {'ordering': '-imdb'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['imdb'], 9.2)
        self.assertEqual(response.data[-1]['imdb'], 7.8)