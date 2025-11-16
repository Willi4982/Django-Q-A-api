from rest_framework import generics, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Question, Answer
from .serializers import QuestionSerializer, AnswerSerializer


class QuestionListCreateView(generics.ListCreateAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer


class QuestionRetrieveDeleteView(generics.RetrieveDestroyAPIView):
	queryset = Question.objects.all()
	serializer_class = QuestionSerializer


class AnswerCreateView(generics.CreateAPIView):
	serializer_class = AnswerSerializer

	def create(self, request, *args, **kwargs):
		question_id = kwargs.get("question_id")
		question = get_object_or_404(Question, pk=question_id)
		serializer = self.get_serializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		answer = Answer.objects.create(
			question=question,
			user_id=serializer.validated_data["user_id"],
			text=serializer.validated_data["text"],
		)
		headers = self.get_success_headers(serializer.data)
		return Response(AnswerSerializer(answer).data, status=status.HTTP_201_CREATED, headers=headers)


class AnswerRetrieveDeleteView(generics.RetrieveDestroyAPIView):
	queryset = Answer.objects.all()
	serializer_class = AnswerSerializer

