from django.urls import reverse_lazy
from django.db import transaction
from django.views.generic import ListView, DetailView 
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Questionnaire, Quiz, Alternative, SchoolClass, Student
from .forms import QuestionnaireForm, QuizInlineFormSet

class QuestionnaireList(ListView):
    model = Questionnaire 

class QuestionnaireCreate(CreateView):
    model = Questionnaire
    form_class = QuestionnaireForm 
    success_url = reverse_lazy('questionnaire_list')

class QuestionnaireDetail(DetailView):
    model = Questionnaire

class QuestionnaireDelete(DeleteView):
    model = Questionnaire
    success_url = reverse_lazy('questionnaire_list')

class QuizCreate(CreateView):
    model = Quiz
    fields = ['question']
    success_url = reverse_lazy('questionnaire_list')

    def get_context_data(self, **kwargs):
        data = super(QuizCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['inlines'] = QuizInlineFormSet(self.request.POST)
        else:
            data['inlines'] = QuizInlineFormSet()
        return data
    
    def form_valid(self, form):
        context = self.get_context_data()
        inlines = context['inlines']
        with transaction.atomic():
            self.object = form.save()

            if inlines.is_valid():
                inlines.instance = self.object
                inlines.save()
        return super(QuizCreate, self).form_valid(form)

class QuizList(ListView):
	model = Quiz 

class SchoolClassCreate(CreateView):
    model = SchoolClass
    fields = '__all__'
    success_url = reverse_lazy('schoolclass_list')

class SchoolClassList(ListView):
    model = SchoolClass

class SchoolClassDelete(DeleteView):
    model = SchoolClass
    success_url = reverse_lazy('schoolclass_list')

    
