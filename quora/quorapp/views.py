from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer
from django.shortcuts import get_object_or_404



class QuestionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        questions = Question.objects.all().order_by('-created_at')
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Question, pk=pk)

    def get(self, request, pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self, request, pk):
        question = self.get_object(pk)
        if question.author != request.user:
            return Response(
                {'error': 'You are not the author of this question'},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = QuestionSerializer(question, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question = self.get_object(pk)
        if question.author != request.user:
            return Response(
                {'error': 'You are not the author of this question'},
                status=status.HTTP_403_FORBIDDEN
            )
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class AnswerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, question_pk):
        question = get_object_or_404(Question, pk=question_pk)
        serializer = AnswerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(question=question, author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LikeAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, answer_pk):
        answer = get_object_or_404(Answer, pk=answer_pk)
        if request.user in answer.likes.all():
            answer.likes.remove(request.user)
            message = 'Answer unliked'
        else:
            answer.likes.add(request.user)
            message = 'Answer liked'
        serializer = AnswerSerializer(answer)
        return Response({'message': message, 'answer': serializer.data})