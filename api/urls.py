from django.urls import path
from .views import (
    QuizListCreateView,
    QuizRetrieveUpdateDestroyView,
    OptionListCreateView,
    OptionRetrieveUpdateDestroyView,
    QuestionListCreateView,
    QuestionRetrieveUpdateDestroyView,
    CandidateRetrieveUpdateDestroyView,
    CandidateCreateView,
    QuizListCreateView,
)

urlpatterns = [
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='quiz-detail'),
    
    path('options/', OptionListCreateView.as_view(), name='option-list-create'),
    path('options/<int:pk>/', OptionRetrieveUpdateDestroyView.as_view(), name='option-detail'),
    
    path('candidate/', CandidateCreateView.as_view(), name='candidate-list-create'),
    path('candidate/<int:pk>/', CandidateRetrieveUpdateDestroyView.as_view(), name='option-detail'),

    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-detail'),
]
