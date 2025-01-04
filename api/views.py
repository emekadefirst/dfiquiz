from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import Quiz, Option, Question
from .serializers import QuizSerializer, OptionSerializer, QuestionSerializer


# Quiz Views
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


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
