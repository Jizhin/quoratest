from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('question/<int:question_id>/answer/' , views.post_answer , name='post_answer') ,
    path('like/<int:answer_id>/', views.like_answer, name='like_answer'),
]
