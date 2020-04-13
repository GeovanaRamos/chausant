from django.contrib import admin
from .models import Quiz, Alternative, Questionnaire, User, Teacher, Student

admin.site.register(Questionnaire)
admin.site.register(Quiz)
admin.site.register(Alternative)
admin.site.register(User)
admin.site.register(Teacher)
admin.site.register(Student)
