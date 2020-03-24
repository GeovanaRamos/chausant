from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionnaireList.as_view(), name='questionnaire_list'),
    path('create', views.QuestionnaireCreate.as_view(), name='questionnaire_create'),
    path('quiz/create', views.QuizCreate.as_view(), name='quiz_create'),
    path('quiz', views.QuizList.as_view(), name='quiz_list'),
    path("schoolclass", views.SchoolClassList.as_view(), name="schoolclass_list"),
    path("schoolclass/create", views.SchoolClassCreate.as_view(), name="schoolclass_create"),
    path("students/pending", views.PendingStudentsList.as_view(), name="pending_students_list")
]