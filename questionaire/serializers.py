from rest_framework import serializers
from .models import *
from rest_framework.validators import ValidationError
from candidate.models import Candidate


class QuizSerializer(serializers.ModelSerializer):
    examiner = serializers.SlugRelatedField(slug_field="name", queryset=Candidate.objects.all())
    class Meta:
        model = Quiz
        fields = ['id', 'examiner', 'name', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        return Quiz.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.examiner = validated_data.get("examiner", instance.examiner)
        return instance


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ["id", "option", "is_correct"]
        read_only_fields = ["id"]


class QuestionSerializer(serializers.ModelSerializer):
    quiz = serializers.SlugRelatedField(slug_field="name", queryset=Quiz.objects.all())
    options = OptionSerializer(many=True)

    class Meta:
        model = Question
        fields = ["id", "quiz", "question", "options"]
        read_only_fields = ["id"]

    def create(self, validated_data):
        options_data = validated_data.pop("options")  
        question = Question.objects.create(**validated_data)  

        for option_data in options_data:
            Option.objects.create(question=question, **option_data)  
        return question

    def update(self, instance, validated_data):
        options_data = validated_data.pop("options", None)  

        instance.quiz = validated_data.get("quiz", instance.quiz)
        instance.question = validated_data.get("question", instance.question)
        instance.save()

        if options_data is not None:
            
            instance.option.clear()  
            for option_data in options_data:
                Option.objects.create(question=instance, **option_data)  
        return instance

class CandidateAttemptSerializer(serializers.ModelSerializer):
    candidate = serializers.SlugRelatedField(slug_field="full_name", queryset=Candidate.objects.all())
    question = serializers.SlugRelatedField(slug_field="question", queryset=Question.objects.all())
    selected_option = serializers.SlugRelatedField(slug_field="question", queryset=Option.objects.all())
    class Meta:
        model = CandidateAttempt
        fields = ["id", "candidate", "question", "selected_option", "score"]
        read_only_fields = ["id", "score"]
