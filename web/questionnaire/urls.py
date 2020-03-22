from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.QuestionnaireList.as_view(), name='questionnaire_list'),
    # path('questionnaire/<int:pk>', views.QuestionnaireDetail.as_view(), name='questionnaire_detail'),
    path('create', views.QuestionnaireCreate.as_view(), name='questionnaire_create'),
    path('quiz/create', views.QuizCreate.as_view(), name='quiz_create'),
    path('quiz', views.QuizList.as_view(), name='quiz_list'),
    # path('update/<int:pk>', views.QuestionnaireUpdate.as_view(), name='questionnaire_update'),
    # path('delete/<int:pk>', views.QuestionnaireDelete.as_view(), name='questionnaire_delete')
]