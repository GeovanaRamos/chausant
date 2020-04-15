from django.core.exceptions import ValidationError


class CustomPasswordValidator:

    def __init__(self, min_length=4):
        self.min_length = min_length

    def validate(self, password, user=None):
        if not any(char.isdigit() for char in password):
            raise ValidationError(
                'Senha deve conter no mínimo %(min_length)d digitos.' % {'min_length': self.min_length})
        if not any(char.isalpha() for char in password):
            raise ValidationError(
                'Senha deve conter no mínimo %(min_length)d letras.' % {'min_length': self.min_length})
