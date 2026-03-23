from rest_framework import serializers
from .models import Review
from django.contrib.auth.models import UserSerializer

class ReviewSerializer(serializers.ModelSerializer):
    writer = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = "__all__"