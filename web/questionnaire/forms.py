from django import forms
from django.forms import inlineformset_factory
from .models import Questionnaire, Alternative, Quiz

class QuestionnaireForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Questionnaire
        fields = ['title', 'password']

class AlternativeForm(forms.ModelForm):
     class Meta:
        model = Alternative
        fields = ['text', 'is_answer']

QuizInlineFormSet = inlineformset_factory(Quiz,
    Alternative,
    form=AlternativeForm,
    extra=4,
)