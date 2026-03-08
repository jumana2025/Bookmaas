from rest_framework.routers import DefaultRouter
from .views import WritingViewSet, CommentViewSet, ConversationViewSet, MessageViewSet, UserViewSet

router = DefaultRouter()
router.register(r'writings', WritingViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'conversations', ConversationViewSet, basename='conversation')
router.register(r'messages', MessageViewSet)
router.register(r'users', UserViewSet, basename='user')

urlpatterns = router.urls
