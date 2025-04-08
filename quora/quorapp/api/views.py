from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Question , Answer
from ..serializers import QuestionSerializer , AnswerSerializer


class QuestionListCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self , request):
        questions = Question.objects.all().order_by('-created_at')
        serializer = QuestionSerializer(questions , many=True)
        return Response(serializer.data)

    def post(self , request):
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self , pk):
        return get_object_or_404(Question , pk=pk)

    def get(self , request , pk):
        question = self.get_object(pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data)

    def put(self , request , pk):
        question = self.get_object(pk)
        if question.author != request.user:
            return Response(
                {'error': 'You are not the author of this question'} ,
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = QuestionSerializer(question , data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)

    def delete(self , request , pk):
        question = self.get_object(pk)
        if question.author != request.user:
            return Response(
                {'error': 'You are not the author of this question'} ,
                status=status.HTTP_403_FORBIDDEN
            )
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AnswerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request , question_pk=None):
        # Handle both standalone and question-specific answer creation
        data = request.data.copy()
        if question_pk:
            data['question'] = question_pk

        serializer = AnswerSerializer(data=data , context={'request': request})
        if serializer.is_valid():
            answer = serializer.save(author=request.user)
            if question_pk:
                answer.question = get_object_or_404(Question , pk=question_pk)
                answer.save()
            return Response(serializer.data , status=status.HTTP_201_CREATED)
        return Response(serializer.errors , status=status.HTTP_400_BAD_REQUEST)


class LikeAnswerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self , request , pk):
        answer = get_object_or_404(Answer , pk=pk)
        user = request.user

        if user in answer.likes.all():
            answer.likes.remove(user)
            action = 'unliked'
        else:
            answer.likes.add(user)
            action = 'liked'

        serializer = AnswerSerializer(answer , context={'request': request})
        return Response({
            'status': f'Answer {action} successfully' ,
            'answer': serializer.data ,
            'like_count': answer.likes.count() ,
            'is_liked': user in answer.likes.all()
        })