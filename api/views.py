from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from random import sample
from rest_framework.decorators import action
from .models import Quiz, Option, Question, Candidate, Session, Result
from .serializers import (
    QuizSerializer,
    OptionSerializer,
    QuestionSerializer,
    CandidateSerializer,
    SessionSerializer,
    ResultSerilaizer,
)

# session
class SesionCreateView(generics.ListCreateAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


class SessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer


# Candidate view
class CandidateCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class QuizListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuestionCreateView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer





# Option Views
class OptionListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


class OptionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Option.objects.all()
    serializer_class = OptionSerializer


# Question Views
class QuestionListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
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
    # permission_classes = [IsAuthenticated]
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# candidate
class CandidateListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateListCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


class CandidateRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer


from rest_framework.views import APIView
import pandas as pd


class UploadQuestionsView(APIView):
    # permission_classes = [IsAuthenticated]
    def post(self, request):
        file = request.FILES["file"]
        df = pd.read_excel(file)

        questions_data = []
        for _, row in df.iterrows():
            question = {
                "text": row["Question Text"],
                "quiz": row["Quiz Name"],
                "options": [
                    {"text": row["Option 1"], "is_correct": row["Is Option 1 Correct"]},
                    {"text": row["Option 2"], "is_correct": row["Is Option 2 Correct"]},
                    {"text": row["Option 3"], "is_correct": row["Is Option 3 Correct"]},
                    {"text": row["Option 4"], "is_correct": row["Is Option 4 Correct"]},
                ],
            }
            questions_data.append(question)

        serializer = QuestionSerializer(data=questions_data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Questions uploaded successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SessionQuestion(APIView):
    def get(self, request, phone_number: str, code: str):
        # Check if the candidate exists
        candidate = Candidate.objects.filter(phone_number=phone_number).first()
        if not candidate:
            return Response(
                {"message": "You are not registered for this test"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Check if the session exists for the candidate with the given code
        session = Session.objects.filter(candidates=candidate, code=code).first()
        if not session:
            return Response(
                {"message": "Invalid session code"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Get all questions for the quiz
        quiz = session.quiz
        questions = list(Question.objects.filter(quiz=quiz))

        # Shuffle and limit the questions to the session's number_of_question
        shuffled_questions = sample(
            questions, min(len(questions), session.number_of_question)
        )

        # Serialize and return the questions
        serializer = QuestionSerializer(shuffled_questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ResultCreateView(generics.ListCreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Result.objects.all()
    serializer_class = ResultSerilaizer


class ResultRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Result.objects.all()
    serializer_class = ResultSerilaizer


class CountView(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        candidate = Candidate.objects.count()
        quiz = Quiz.objects.count()
        session = Session.objects.count()
        question = Question.objects.count()
        return Response({"candidate_count": candidate, "quiz_count": quiz, "session_count": session, "question_count": question}, status=status.HTTP_200_OK)
