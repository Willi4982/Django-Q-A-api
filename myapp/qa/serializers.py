from rest_framework import serializers
from .models import Question, Answer


class AnswerSerializer(serializers.ModelSerializer):
	def validate_user_id(self, value: str) -> str:
		if not value or not value.strip():
			raise serializers.ValidationError("user_id must not be empty.")
		return value

	def validate_text(self, value: str) -> str:
		if not value or not value.strip():
			raise serializers.ValidationError("Text must not be empty.")
		return value

	class Meta:
		model = Answer
		fields = ["id", "question", "user_id", "text", "created_at"]
		read_only_fields = ["id", "created_at", "question"]


class QuestionSerializer(serializers.ModelSerializer):
	answers = AnswerSerializer(many=True, read_only=True)

	def validate_text(self, value: str) -> str:
		if not value or not value.strip():
			raise serializers.ValidationError("Text must not be empty.")
		return value

	class Meta:
		model = Question
		fields = ["id", "text", "created_at", "answers"]
		read_only_fields = ["id", "created_at", "answers"]

