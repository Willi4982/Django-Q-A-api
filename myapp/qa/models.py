from django.db import models


class Question(models.Model):
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["-created_at", "-id"]

	def __str__(self) -> str:
		return f"Question #{self.pk}"


class Answer(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
	user_id = models.CharField(max_length=64)
	text = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		ordering = ["created_at", "id"]

	def __str__(self) -> str:
		return f"Answer #{self.pk} to Q{self.question_id}"

