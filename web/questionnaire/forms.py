from django import forms
from django.forms import inlineformset_factory
from .models import Questionnaire, Alternative, Quiz, User, SchoolClass
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomUserCreationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

    class Meta(UserCreationForm):
        model = User
        fields = ('request_type', 'full_name', 'email', 'password1', 'password2')


class SchoolClassForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = SchoolClass
        fields = '__all__'


class QuestionnaireForm(forms.ModelForm):
    class Meta:
        model = Questionnaire
        fields = ('title', 'school_classes', 'start_date', 'due_date', 'quizzes')


class AlternativeForm(forms.ModelForm):
    class Meta:
        model = Alternative
        fields = ('text', 'is_answer')


QuizInlineFormSet = inlineformset_factory(Quiz,
                                          Alternative,
                                          form=AlternativeForm,
                                          extra=4,
                                          can_delete=False
                                          )
