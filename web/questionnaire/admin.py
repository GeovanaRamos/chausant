from django.contrib import admin
from .models import Quiz, Alternative, Questionnaire

admin.site.register(Questionnaire)
admin.site.register(Quiz)
admin.site.register(Alternative)
