from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Questionnaire, Quiz, Alternative
from .forms import QuestionnaireForm

class QuestionnaireList(ListView):
	model = Questionnaire 

class QuestionnaireUpdate(UpdateView):
	model = Questionnaire 

class QuestionnaireDelete(DeleteView):
	model = Questionnaire

class QuestionnaireDetail(DetailView):
	model = Questionnaire

class QuestionnaireCreate(CreateView):
	model = Questionnaire
	form_class = QuestionnaireForm

# class QuizList(ListView):
# 	model = Quiz 

# class QuizUpdate(UpdateView):
# 	model = Quiz 

# class QuizDelete(DeleteView):
# 	model = Quiz

# class AlternativeList(ListView):
# 	model = Alternative 

# class ALternativeUpdate(UpdateView):
# 	model = Alternative 

# class ALternativeDelete(DeleteView):
# 	model = Alternative