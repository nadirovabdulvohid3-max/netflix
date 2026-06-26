from rest_framework.routers import DefaultRouter
from .views import ActorViewSet

router = DefaultRouter()
router.register(r'actor', ActorViewSet)

urlpatterns = router.urls