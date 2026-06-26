from rest_framework import viewsets, status
from rest_framework.decorators import action
from .models import Movie, Actor
from .serializers import MovieDetailSerializer, MovieWriteSerializer, CommentSerializer
from Actor.serializers import ActorSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Comment
from .serializers import CommentSerializer
from rest_framework.filters import SearchFilter,OrderingFilter


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'genre']
    ordering_fields = ['imdb']
    ordering = ['-imdb']
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return MovieWriteSerializer
        return MovieDetailSerializer

    @action(detail=True, methods=['POST'], url_path='add-actor')
    def add_actor(self, request, pk=None):
        movie = self.get_object()
        actor_id = request.data.get('actor_id')
        try:
            actor = Actor.objects.get(id=actor_id)
        except Actor.DoesNotExist:
            return Response(
                {"error": f"ID={actor_id} bo'lgan aktyor topilmadi!"},
                status=status.HTTP_404_NOT_FOUND)
        if movie.actors.filter(id=actor.id).exists():
            return Response(
                {"message": "Bu aktyor filmga allaqachon qo'shilgan!"},
                status=status.HTTP_400_BAD_REQUEST)
        movie.actors.add(actor)
        return Response(
            {"message": f"{actor.name} muvaffaqiyatli qo'shildi"},
            status=status.HTTP_200_OK)

class MovieActorAPIView(APIView):
    def get(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
        except Movie.DoesNotExist:
            return Response(
                {"error": f"ID={id} bo'lgan kino topilmadi!"},
                status=status.HTTP_404_NOT_FOUND)
        actors = movie.actors.all()
        serializer = ActorSerializer(actors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(
                {"message": "izoh muvaffaqiyatli qo'shiladi", "data": serializer.data},
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CommentDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, pk, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=pk)
        except Comment.DoesNotExist:
            return Response(
                {"error": "Bunday komment topilmadi!"},
                status=status.HTTP_404_NOT_FOUND
            )

        if comment.user != request.user:
            return Response(
                {"error": "Siz faqat o'zingiz yozgan kommentni o'chira olasiz!"},
                status=status.HTTP_403_FORBIDDEN
            )
        comment.delete()

        return Response(
            {"message": "Komment muvaffaqiyatli o'chirildi!"},
            status=status.HTTP_200_OK
        )