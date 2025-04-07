from rest_framework import serializers
from .models import Question , Answer
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id' , 'username']


class QuestionSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id' , 'title' , 'content' , 'author' , 'created_at' , 'updated_at', 'answers']

    def get_answers(self, obj):
        answers = obj.answers.all().order_by('-created_at')
        serializer = AnswerSerializer(answers , many=True)
        return serializer.data


class AnswerSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    likes = UserSerializer(many=True , read_only=True)
    like_count = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id' , 'content' , 'question' , 'author' , 'created_at' , 'updated_at' , 'likes' , 'like_count']

    def get_like_count(self , obj):
        return obj.likes.count()