from django.urls import path
from django.views.generic import RedirectView
from .views import (
	QuestionListCreateView,
	QuestionRetrieveDeleteView,
	AnswerCreateView,
	AnswerRetrieveDeleteView,
)
from .web_views import UIQuestionsList, UIQuestionDetail, ui_create_question, ui_add_answer, ui_delete_question, ui_delete_answer

urlpatterns = [
	path("", RedirectView.as_view(url="/ui/questions/", permanent=False)),
	path("ui/", RedirectView.as_view(url="/ui/questions/", permanent=False)),
	path("ui/questions/", UIQuestionsList.as_view(), name="ui-questions"),
	path("ui/questions/<int:pk>/", UIQuestionDetail.as_view(), name="ui-question-detail"),
	path("ui/questions/create/", ui_create_question, name="ui-question-create"),
	path("ui/questions/<int:pk>/answers/create/", ui_add_answer, name="ui-answer-create"),
	path("ui/questions/<int:pk>/delete/", ui_delete_question, name="ui-question-delete"),
	path("ui/questions/<int:pk>/answers/<int:answer_id>/delete/", ui_delete_answer, name="ui-answer-delete"),
	path("questions/", QuestionListCreateView.as_view(), name="question-list-create"),
	path("questions/<int:pk>/", QuestionRetrieveDeleteView.as_view(), name="question-detail-delete"),
	path("questions/<int:question_id>/answers/", AnswerCreateView.as_view(), name="answer-create"),
	path("answers/<int:pk>/", AnswerRetrieveDeleteView.as_view(), name="answer-detail-delete"),
]

