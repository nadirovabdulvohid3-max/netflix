from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MovieViewSet, MovieActorAPIView, CommentCreateAPIView, CommentListAPIView, CommentDeleteAPIView

router = DefaultRouter()
router.register(r'movies', MovieViewSet)

urlpatterns = [
    path('movies/<int:id>/actors/', MovieActorAPIView.as_view(), name='movie-actors'),
    path('comments/create/', CommentCreateAPIView.as_view(), name='comment-create'),
    path('comments/list/', CommentListAPIView.as_view(), name='comment-list'),

    path('comments/<int:pk>/delete/', CommentDeleteAPIView.as_view(), name='comment-delete'),  # 👈 Qo'shildi

    path('', include(router.urls)),
]