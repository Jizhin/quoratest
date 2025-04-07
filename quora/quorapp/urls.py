from django.urls import path
from .views import (
    QuestionListCreateAPIView,
    QuestionDetailAPIView,
    AnswerCreateAPIView,
    LikeAnswerAPIView
)

urlpatterns = [
    path('questions/', QuestionListCreateAPIView.as_view(), name='question-list'),
    path('questions/<int:pk>/', QuestionDetailAPIView.as_view(), name='question-detail'),
    path('questions/<int:question_pk>/answers/', AnswerCreateAPIView.as_view(), name='answer-create'),
    path('answers/<int:answer_pk>/like/', LikeAnswerAPIView.as_view(), name='answer-like'),
]