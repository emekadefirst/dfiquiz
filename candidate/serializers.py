from rest_framework import serializers
from .models import Candidate


class CreateCandidateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "other_name",
            "candidate_id",
            "email",
            "username",
            "password",
            "full_name"
        ]
        read_only_fields = ["id", 'full_name']

    def create(self, validated_data):
        password = validated_data.pop("password")
        candidate = Candidate(**validated_data)
        candidate.set_password(password)
        candidate.save()
        return candidate


class GetCandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ["id", "username", "email", "fullname"]
