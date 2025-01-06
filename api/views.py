from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action

from .models import Quiz, Option, Question, Candidate
from .serializers import QuizSerializer, OptionSerializer, QuestionSerializer, CandidateSerializer


# Candidate view
class CandidateCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    @action(detail=False, methods=['post'])
    def create_question(self, request):
        data = request.data
        quiz_id = data.get('quiz')
        question_text = data.get('text')
        options = data.get('options', [])

        # Ensure the quiz exists
        quiz = Quiz.objects.get(id=quiz_id)

        # Create the question
        question = Question.objects.create(text=question_text, quiz=quiz)

        # Create options
        for option in options:
            Option.objects.create(
                text=option['text'], 
                is_correct=option['is_correct'], 
                question=question
            )
        
        return Response({"message": "Question created successfully"}, status=status.HTTP_201_CREATED)


class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


# Option Views
class OptionListCreateView(generics.ListCreateAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class OptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


# Question Views
class QuestionListCreateView(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    def create(self, request, *args, **kwargs):
        option_data = request.data.pop("option")
        option_serializer = OptionSerializer(data=option_data)
        if option_serializer.is_valid():
            option = option_serializer.save()
            request.data["option"] = option.id
            return super().create(request, *args, **kwargs)
        return Response(option_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# candidate
class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateListCreateView(generics.ListCreateAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
