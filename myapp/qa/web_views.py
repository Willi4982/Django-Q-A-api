from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Question, Answer
from django.views.decorators.http import require_POST


class UIQuestionsList(TemplateView):
	template_name = 'questions_list.html'

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		qs = Question.objects.order_by('-created_at')
		ctx['questions'] = qs
		return ctx


def ui_create_question(request):
	if request.method == 'POST':
		text = (request.POST.get('text') or '').strip()
		if not text:
			messages.error(request, 'Текст вопроса не может быть пустым.')
			return redirect('ui-questions')
		q = Question.objects.create(text=text)
		messages.success(request, 'Вопрос создан.')
		return redirect('ui-question-detail', pk=q.id)
	return redirect('ui-questions')


class UIQuestionDetail(TemplateView):
	template_name = 'question_detail.html'

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		q = get_object_or_404(Question, pk=kwargs['pk'])
		ctx['question'] = q
		ctx['answers'] = q.answers.order_by('created_at')
		return ctx


def ui_add_answer(request, pk: int):
	if request.method == 'POST':
		user_id = (request.POST.get('user_id') or '').strip()
		text = (request.POST.get('text') or '').strip()
		if not user_id or not text:
			messages.error(request, 'user_id и текст ответа обязательны.')
			return redirect('ui-question-detail', pk=pk)
		question = get_object_or_404(Question, pk=pk)
		Answer.objects.create(question=question, user_id=user_id, text=text)
		messages.success(request, 'Ответ добавлен.')
	return redirect('ui-question-detail', pk=pk)


@require_POST
def ui_delete_question(request, pk: int):
	question = get_object_or_404(Question, pk=pk)
	question.delete()
	messages.success(request, 'Вопрос удалён.')
	return redirect('ui-questions')


@require_POST
def ui_delete_answer(request, pk: int, answer_id: int):
	question = get_object_or_404(Question, pk=pk)
	answer = get_object_or_404(Answer, pk=answer_id, question=question)
	answer.delete()
	messages.success(request, 'Ответ удалён.')
	return redirect('ui-question-detail', pk=pk)


