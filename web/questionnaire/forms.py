from django import forms
from django.forms import inlineformset_factory
from .models import Questionnaire, Alternative, Quiz, User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Nome e/ou senha incorretos. ",
        'inactive': "Esta conta não foi validada.",
    }

    def __init__(self, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        self.fields['password'].label = "Senha"


class CustomUserCreationForm(UserCreationForm):
    error_messages = {
        'password_mismatch': "Confirmação de senha diferente",
    }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for fieldname in ['password1', 'password2']:
            self.fields[fieldname].help_text = None

        self.fields['password1'].label = "Senha"
        self.fields['password2'].label = "Confirmar Senha"

    class Meta(UserCreationForm):
        model = User
        fields = ('request_type', 'full_name', 'email', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email já cadastrado.")
        return email


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
