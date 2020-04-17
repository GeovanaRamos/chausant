from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('', views.QuestionnaireList.as_view(), name='questionnaire_list'),
    path('questionnaire/create', views.QuestionnaireCreate.as_view(), name='questionnaire_create'),
    path('questionnaire/update/<pk>', views.QuestionnaireUpdate.as_view(), name='questionnaire_update'),
    path('quiz/create', views.QuizCreate.as_view(), name='quiz_create'),
    path('quiz', views.QuizList.as_view(), name='quiz_list'),
    path("schoolclass", views.SchoolClassList.as_view(), name="schoolclass_list"),
    path("schoolclass/create", views.SchoolClassCreate.as_view(), name="schoolclass_create"),
    path("schoolclass/delete/<pk>", views.SchoolClassDelete.as_view(), name="schoolclass_delete"),
    path("schoolclass/add/student", views.AddSchoolClassToStudent.as_view(), name="add_school_class_to_student"),
    path("detail/<pk>", views.QuestionnaireDetail.as_view(), name="questionnaire_detail"),
    path("delete/<pk>", views.QuestionnaireDelete.as_view(), name="questionnaire_delete"),
    path("quiz/delete/<pk>", views.QuizDelete.as_view(), name="quiz_delete"),
    path("quiz/list/<questionnaire_pk>", views.QuizStudentList.as_view(), name="quiz_student_list"),
    path("quizresult/create", views.QuizResultCreate.as_view(), name="quizresult_create"),
    path('signup', views.SignUp.as_view(), name='sign_up'),
    path('signin', LoginView.as_view(template_name='registration/sign_in.html'), name='sign_in'),
    path('profile/<pk>', views.UserDetail.as_view(), name="user_detail"),
    path('profile/update/<pk>', views.UserUpdate.as_view(), name="user_update"),
    path('students/<school_class_pk>', views.SchoolClassStudentList.as_view(), name="student_list")
]
