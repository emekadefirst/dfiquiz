from .models import Quiz, Option, Question, Candidate, Response, Session, Result
from rest_framework import serializers

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'created_at']
        read_only = ['id', "created_at"]

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
    class Meta:
        model = Option
        fields = ["text", "is_correct"]


class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)  # Change 'option' to 'options'
    quiz = serializers.SlugRelatedField(slug_field="name", queryset=Quiz.objects.all())

    class Meta:
        model = Question
        fields = ["id", "text", "quiz", "options"]  # Change 'option' to 'options'
        read_only_fields = ["id"]

    def create(self, validated_data):
        options_data = validated_data.pop("options")  # Change 'option' to 'options'
        question = Question.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(question=question, **option_data)
        return question


class ResponseSerializer(serializers.ModelSerializer):
    candidate = serializers.SlugRelatedField(slug_field="phone_number", queryset=Candidate.objects.all())
    question = serializers.SlugRelatedField(slug_field="id", queryset=Question.objects.all())
    selected_option = serializers.SlugRelatedField(slug_field="text", queryset=Quiz.objects.all())
    class Meta:
        model = Response
        fields = ["candidate", "question", "selected_option", "count"]
        read_only_fields = ["count"]

    def create(self, validated_data):
        return Question.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class BulkQuestionSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        questions = [Question(**item) for item in validated_data]
        return Question.objects.bulk_create(questions)


class BulkUploadQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "text", "quiz", "options"]
        list_serializer_class = BulkQuestionSerializer


class SessionSerializer(serializers.ModelSerializer):
    quiz = serializers.SlugRelatedField(slug_field="name", queryset=Quiz.objects.all())
    candidates = serializers.SlugRelatedField(
        many=True,
        slug_field="phone_number",
        queryset=Candidate.objects.all(),
        required=False,
    )

    class Meta:
        model = Session
        fields = [
            "id",
            "start_time",
            "end_time",
            "code",
            "quiz",
            "candidates",
            "created_at",
            "number_of_question",
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        # Replace the 'candidates' field with detailed candidate information
        representation["candidates"] = CandidateSerializer(
            instance.candidates.all(), many=True
        ).data
        return representation

    def create(self, validated_data):
        candidates = validated_data.pop("candidates", [])
        session_instance = Session.objects.create(**validated_data)
        if candidates:
            session_instance.candidates.set(candidates)
        return session_instance


class ResultSerilaizer(serializers.ModelSerializer):
    quiz = serializers.SlugRelatedField(slug_field="name", queryset=Quiz.objects.all())
    candidate = serializers.SlugRelatedField(slug_field="phone_number", queryset=Candidate.objects.all())
    session_code = serializers.SlugRelatedField(slug_field="code", queryset=Session.objects.all())
    full_name = serializers.SerializerMethodField()


    class Meta:
        model = Result
        fields = ["id", "candidate", "session_code", "quiz", "score", "full_name"]
        read_only_fields = ["id"]

    def get_full_name(self, obj):
        return f"{obj.candidate.first_name} {obj.candidate.last_name}"

    def create(self, validated_data):
        return Result.objects.create(**validated_data)

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
