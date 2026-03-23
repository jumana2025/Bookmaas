from rest_framework import serializers
from .models import Writing, Comment, Conversation, Message
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class WritingSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)

    class Meta:
        model = Writing
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username', read_only=True)

    class Meta:
        model = Message
        fields = ['id', 'conversation', 'sender', 'sender_username', 'content', 'created_at']


class ConversationSerializer(serializers.ModelSerializer):
    user1_username = serializers.CharField(source='user1.username', read_only=True)
    user2_username = serializers.CharField(source='user2.username', read_only=True)
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Conversation
        fields = [
            'id',
            'user1',
            'user1_username',
            'user2',
            'user2_username',
            'messages',
            'created_at',
            'updated_at'
        ]