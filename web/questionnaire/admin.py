from django.contrib import admin
from .models import Quiz, Alternative, Questionnarie

admin.site.register(Questionnarie)
admin.site.register(Quiz)
admin.site.register(Alternative)
