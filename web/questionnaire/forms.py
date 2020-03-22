from django import forms
from .models import Questionnaire

class QuestionnaireForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = Questionnaire
        fields = ['title', 'password']
