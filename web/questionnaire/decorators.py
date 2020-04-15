from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import REDIRECT_FIELD_NAME


def student_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='sign_in'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'student'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def teacher_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='sign_in'):

    actual_decorator = user_passes_test(
        lambda u: u.is_active and hasattr(u, 'teacher'),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
