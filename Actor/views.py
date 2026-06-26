from rest_framework.generics import ListAPIView
from .models import Actor
from .serializers import ActorSerializer
from rest_framework.viewsets import ModelViewSet

class ActorAPIView(ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer

class ActorViewSet(ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer