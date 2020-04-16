import json
from django.urls import reverse_lazy
from django.db import transaction
from django.http import JsonResponse
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from .models import Questionnaire, Quiz, Alternative, SchoolClass, User, QuizResult
from .forms import QuestionnaireForm, QuizInlineFormSet, CustomUserCreationForm, SchoolClassForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .decorators import student_required, teacher_required
from django.utils.decorators import method_decorator


class QuestionnaireList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('sign_in')
    model = Questionnaire

    def get_queryset(self):
        if hasattr(self.request.user, 'student'):
            student = self.request.user.student
            return Questionnaire.objects.filter(school_classes__id__in=student.get_classes())
        elif hasattr(self.request.user, 'teacher'):
            teacher = self.request.user.teacher
            return Questionnaire.objects.filter(school_classes__id__in=teacher.get_classes())

        return Questionnaire.objects.none()


@method_decorator([teacher_required], name='dispatch')
class QuestionnaireCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('sign_in')
    model = Questionnaire
    form_class = QuestionnaireForm
    success_url = reverse_lazy('questionnaire_list')
    # TODO correct date and time input


class QuestionnaireDetail(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('sign_in')
    model = Questionnaire


@method_decorator([teacher_required], name='dispatch')
class QuestionnaireDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sign_in')
    model = Questionnaire
    success_url = reverse_lazy('questionnaire_list')


@method_decorator([teacher_required], name='dispatch')
class QuizCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('sign_in')
    model = Quiz
    fields = ['title', 'question']
    success_url = reverse_lazy('quiz_list')

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

        self.object = form.save(commit=False)
        self.object.teacher = self.request.user.teacher
        self.object.save()

        with transaction.atomic():
            self.object = form.save()

            if inlines.is_valid():
                inlines.instance = self.object
                inlines.save()

        return super(QuizCreate, self).form_valid(form)


@method_decorator([teacher_required], name='dispatch')
class QuizList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('sign_in')
    model = Quiz

    def get_queryset(self):
        return Quiz.objects.filter(teacher=self.request.user.teacher)


@method_decorator([student_required], name='dispatch')
class QuizStudentList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('sign_in')
    model = Quiz
    template_name = "questionnaire/quiz_student_list.html"

    def get_context_data(self, **kwargs):
        context = super(QuizStudentList, self).get_context_data(**kwargs)
        questionnaire = Questionnaire.objects.get(pk=self.kwargs.get('questionnaire_pk'))
        context['qt_pk'] = questionnaire.pk
        return context

    def get_queryset(self):
        questionnaire = Questionnaire.objects.get(pk=self.kwargs.get('questionnaire_pk'))
        return questionnaire.quizzes.all()


@method_decorator([teacher_required], name='dispatch')
class QuizDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sign_in')
    model = Quiz
    success_url = reverse_lazy('quiz_list')


@method_decorator([teacher_required], name='dispatch')
class SchoolClassCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('sign_in')
    form_class = SchoolClassForm
    success_url = reverse_lazy('schoolclass_list')


@method_decorator([teacher_required], name='dispatch')
class SchoolClassList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('sign_in')
    model = SchoolClass

    def get_queryset(self):
        return self.request.user.teacher.get_classes()


@method_decorator([teacher_required], name='dispatch')
class SchoolClassDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('sign_in')
    model = SchoolClass
    success_url = reverse_lazy('schoolclass_list')


class QuizResultCreate(LoginRequiredMixin, View):
    login_url = reverse_lazy('sign_in')

    def post(self, request):
        print(request.POST)
        questionnaire = request.POST.get('questionnaire')
        answers = json.loads(request.POST.get('answers'))
        print(answers)
        print(questionnaire)
        for key, value in answers.items():
            QuizResult.objects.create(
                questionnaire=Questionnaire.objects.get(pk=questionnaire),
                student=request.user.student,
                quiz=Quiz.objects.get(pk=key),
                is_correct=Alternative.objects.get(pk=value).is_answer
            )
        return JsonResponse({"message":"done"})


class SignUp(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('sign_in')
    template_name = 'registration/sign_up.html'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if self.object.request_type == User.TEACHER:
            self.object.is_active = False
        self.object.username = self.object.full_name.split(' ')[0]
        self.object.save()
        return super(SignUp, self).form_valid(form)
