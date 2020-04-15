from django.urls import path
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm
from . import views

urlpatterns = [
    path('', views.QuestionnaireList.as_view(), name='questionnaire_list'),
    path('create', views.QuestionnaireCreate.as_view(), name='questionnaire_create'),
    path('quiz/create', views.QuizCreate.as_view(), name='quiz_create'),
    path('quiz', views.QuizList.as_view(), name='quiz_list'),
    path("schoolclass", views.SchoolClassList.as_view(), name="schoolclass_list"),
    path("schoolclass/create", views.SchoolClassCreate.as_view(), name="schoolclass_create"),
    path("schoolclass/delete/<pk>", views.SchoolClassDelete.as_view(), name="schoolclass_delete"),
    path("detail/<pk>", views.QuestionnaireDetail.as_view(), name="questionnaire_detail"),
    path("delete/<pk>", views.QuestionnaireDelete.as_view(), name="questionnaire_delete"),
    path("quiz/delete/<pk>", views.QuizDelete.as_view(), name="quiz_delete"),
    path("quiz/list/<questionnaire_pk>/", views.QuizStudentList.as_view(), name="quiz_student_list"),
    path("quizresult/create/", views.QuizResultCreate.as_view(), name="quizresult_create"),
    path('signup/', views.SignUp.as_view(), name='sign_up'),
    path('signin/', LoginView.as_view(
        template_name='registration/sign_in.html', authentication_form=CustomAuthenticationForm), name='sign_in'),
]
