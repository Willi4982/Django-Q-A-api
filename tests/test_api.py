import pytest
from django.urls import reverse
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_create_and_get_question():
	client = APIClient()
	# Create question
	resp = client.post(reverse("question-list-create"), {"text": "What is FastAPI?"}, format="json")
	assert resp.status_code == 201 or resp.status_code == 200
	q_id = resp.data["id"]

	# Retrieve with answers list
	resp = client.get(reverse("question-detail-delete", kwargs={"pk": q_id}))
	assert resp.status_code == 200
	assert resp.data["text"] == "What is FastAPI?"
	assert resp.data["answers"] == []


@pytest.mark.django_db
def test_add_answer_and_fetch():
	client = APIClient()
	q = client.post(reverse("question-list-create"), {"text": "What is Django?"}, format="json").data
	resp = client.post(reverse("answer-create", kwargs={"question_id": q["id"]}), {"user_id": "u1", "text": "A web framework"}, format="json")
	assert resp.status_code == 201
	answer_id = resp.data["id"]

	# Fetch answer
	resp = client.get(reverse("answer-detail-delete", kwargs={"pk": answer_id}))
	assert resp.status_code == 200
	assert resp.data["text"] == "A web framework"


@pytest.mark.django_db
def test_add_answer_to_nonexistent_question_returns_404():
	client = APIClient()
	resp = client.post(
		reverse("answer-create", kwargs={"question_id": 999999}),
		{"user_id": "user-x", "text": "hello"},
		format="json",
	)
	assert resp.status_code == 404


@pytest.mark.django_db
def test_empty_user_id_returns_400():
	client = APIClient()
	q = client.post(reverse("question-list-create"), {"text": "Q"}, format="json").data
	# empty string
	resp = client.post(
		reverse("answer-create", kwargs={"question_id": q["id"]}),
		{"user_id": "   ", "text": "answer"},
		format="json",
	)
	assert resp.status_code == 400
	assert "user_id" in resp.data


@pytest.mark.django_db
def test_cascade_delete_answers_when_question_deleted():
	client = APIClient()
	q = client.post(reverse("question-list-create"), {"text": "Cascade?"}, format="json").data
	# create two answers
	a1 = client.post(reverse("answer-create", kwargs={"question_id": q["id"]}), {"user_id": "u1", "text": "a1"}, format="json").data
	a2 = client.post(reverse("answer-create", kwargs={"question_id": q["id"]}), {"user_id": "u2", "text": "a2"}, format="json").data
	# delete question
	resp = client.delete(reverse("question-detail-delete", kwargs={"pk": q["id"]}))
	assert resp.status_code in (200, 204)
	# answers should be gone
	resp1 = client.get(reverse("answer-detail-delete", kwargs={"pk": a1["id"]}))
	resp2 = client.get(reverse("answer-detail-delete", kwargs={"pk": a2["id"]}))
	assert resp1.status_code == 404
	assert resp2.status_code == 404