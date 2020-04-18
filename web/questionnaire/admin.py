from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import (Quiz, Alternative, Questionnaire, User,
                     Teacher, Student, QuizResult, SchoolClass,
                     Discipline, School)

admin.site.register(Questionnaire)
admin.site.register(Quiz)
admin.site.register(Alternative)
admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(QuizResult)
admin.site.register(SchoolClass)
admin.site.register(School)
admin.site.register(Discipline)


@admin.register(User)
class UserAdmin(DjangoUserAdmin):

    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('full_name', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    ordering = ('email',)
    search_fields = ('email',)