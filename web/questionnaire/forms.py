from django import forms
from django.forms import inlineformset_factory
from .models import Questionnaire, Alternative, Quiz

class QuestionnaireForm(forms.ModelForm):
    
    class Meta:
        model = Questionnaire
        fields = ('title', 'school_classes', 'start_date', 'due_date', 'quizzes' )

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