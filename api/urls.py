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
    QuestionCreateView,
    UploadQuestionsView,
    SesionCreateView,
    SessionRetrieveUpdateDestroyView,
    SessionQuestion,
    ResultCreateView,
    ResultRetrieveUpdateDestroyView,
    CountView,
)

urlpatterns = [
    path('upload-questions/', UploadQuestionsView.as_view(), name='upload-questions'),
    
    path('quizzes/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quizzes/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='quiz-detail'),
    
    path('options/', OptionListCreateView.as_view(), name='option-list-create'),
    path('options/<int:pk>/', OptionRetrieveUpdateDestroyView.as_view(), name='option-detail'),
    
    path('candidate/', CandidateCreateView.as_view(), name='candidate-list-create'),
    path('candidate/<int:pk>/', CandidateRetrieveUpdateDestroyView.as_view(), name='option-detail'),

    path('create-question/', QuestionCreateView.as_view(), name='question'),
    path('questions/', QuestionListCreateView.as_view(), name='question-list-create'),
    path('questions/<int:pk>/', QuestionRetrieveUpdateDestroyView.as_view(), name='question-detail'),
    
    path('session/', SesionCreateView.as_view(), name='session'),
    path('session/<int:pk>/', SessionRetrieveUpdateDestroyView.as_view(), name='session-detail'),
    
    path("result/", ResultCreateView.as_view(), name='all-results'),
    path("result/<int:pk>/", ResultRetrieveUpdateDestroyView.as_view(), name='result-details'),
    
    path('count/', CountView.as_view(), name="count"),
    
    path('question-by-session/<str:phone_number>/<str:code>/', SessionQuestion.as_view(), name='question-by-session'),
]
