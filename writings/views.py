from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import models
from .models import Writing, Comment, Conversation, Message
from .serializers import WritingSerializer, CommentSerializer, ConversationSerializer, MessageSerializer, UserSerializer


class WritingViewSet(viewsets.ModelViewSet):
    queryset = Writing.objects.all().order_by('-created_at')
    serializer_class = WritingSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer


class UserViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password)
        return Response({'id': user.id, 'username': user.username, 'email': user.email}, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['get'])
    def list_users(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    
    def get_queryset(self):
        user_id = self.request.query_params.get('user_id')
        if user_id:
            return Conversation.objects.filter(user1_id=user_id) | Conversation.objects.filter(user2_id=user_id)
        return Conversation.objects.all()

    def create(self, request):
        user1_id = request.data.get('user1')
        user2_id = request.data.get('user2')

        # Check if conversation already exists
        conversation = Conversation.objects.filter(
            (models.Q(user1_id=user1_id) & models.Q(user2_id=user2_id)) |
            (models.Q(user1_id=user2_id) & models.Q(user2_id=user1_id))
        ).first()

        if conversation:
            serializer = self.get_serializer(conversation)
            return Response(serializer.data, status=status.HTTP_200_OK)

        conversation = Conversation.objects.create(user1_id=user1_id, user2_id=user2_id)
        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request):
        conversation_id = request.data.get('conversation')
        sender_id = request.data.get('sender')
        content = request.data.get('content')

        conversation = Conversation.objects.get(id=conversation_id)
        message = Message.objects.create(conversation=conversation, sender_id=sender_id, content=content)
        serializer = self.get_serializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
