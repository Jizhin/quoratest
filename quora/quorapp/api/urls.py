from django.urls import path
from . import views

urlpatterns = [
    path('questions/', views.QuestionListCreateAPIView.as_view(), name='api-question-list'),
    path('questions/<int:pk>/', views.QuestionDetailAPIView.as_view(), name='api-question-detail'),
    # Add other API endpoints
    path('answers/', views.AnswerCreateAPIView.as_view(), name='api-answer-create'),
    path('answers/<int:pk>/like/', views.LikeAnswerAPIView.as_view(), name='api-answer-like'),
]