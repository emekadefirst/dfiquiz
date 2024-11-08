from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Examiner
from django.db.models import Q
from django.contrib.auth import authenticate
from django.db.models.functions import Lower
from rest_framework.authtoken.models import Token
from .serializers import GetExaminerSerializer, CreateExaminerSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication


class SignupView(APIView):
    def post(self, request, format=None):
        serializer = CreateExaminerSerializer(data=request.data)
        if serializer.is_valid():
            candidate = serializer.save()
            token = Token.objects.create(user=candidate)
            response_data = {
                "candidate": serializer.data,
                "token": token.key,
                "detail": "Signup was successful",
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request, format=None):
        username = request.data.get("username")  
        password = request.data.get("password")
        candidate = authenticate(request, username=username, password=password)
        if candidate is not None:
            token, created = Token.objects.get_or_create(user=candidate)
            return Response(
                {"token": token.key, "detail": "Login successful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                {"detail": "Invalid username or password"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ExaminerList(APIView):
    def get(self, request):
        obj = Examiner.objects.all()
        serializer = GetExaminerSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
