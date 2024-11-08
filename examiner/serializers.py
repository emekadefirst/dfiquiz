from rest_framework import serializers
from .models import Examiner


class CreateExaminerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Examiner
        fields = ["id", "username", "organization_name", "upload", "image_url", "url", "address", "password"]
        read_only_fields = ["id", "image_url"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        candidate = Examiner(**validated_data)
        candidate.set_password(password)
        candidate.save()
        return candidate

class GetExaminerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Examiner
        fields = [
            "id",
            "organization_name",
            "image_url",
            "url",
            "address",
        ]
