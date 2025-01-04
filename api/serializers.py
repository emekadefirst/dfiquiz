from .models import Quiz, Option, Question, Candidate, Response
from rest_framework import serializers

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"
        read_only = ["id"]
        
    def create(self, validated_data):
        return Candidate.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'name']
        read_only = ['id']

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class OptionSerializer(serializers.ModelSerializer):
    question = serializers.SlugRelatedField(
        slug_field="id", queryset=Question.objects.all()
    )
    class Meta:
        model = Option
        fields = ['text', 'is_correct', 'question']

    def create(self, validated_data):
        return Option.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)
    quiz = serializers.SlugRelatedField(slug_field="name", queryset=Quiz.objects.all())

    class Meta:
        model = Question
        fields = ["id", "text", "quiz", "options"]
        read_only = ["id"]

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class ResponseSerializer(serializers.ModelSerializer):
    candidate = serializers.SlugRelatedField(slug_field="name", queryset=Candidate.objects.all())
    question = serializers.SlugRelatedField(slug_field="id", queryset=Question.objects.all())
    selected_option = serializers.SlugRelatedField(slug_field="text", queryset=Quiz.objects.all())
    class Meta:
        model = Response
        fields = ["candidate", "question", "selected_option", "count"]


    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
