import os.path
import sys
import random
import string
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def create_password():
    return '123abc'


def create_super_user(name, email):

    password = create_password()
    try:
        u = User.objects.create_superuser(email,
                                          password,
                                          request_type=0,
                                          is_active=True,
                                          full_name=name)

        return u

    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")


def create_user(name, email):
    """
    Creates the user and ensures that if any error occurs the
    script does not continue
    """
    password = create_password()

    try:
        u = User.objects.create_user(
            full_name=name,
            email=email,
            password=password,
            request_type=1,
            is_active=True
        )

        return u

    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")

def populate():
    print ('\n----------------------')
    print ('Populating Database...')
    print ('----------------------\n')

    user_1 = create_super_user('admin', 'admin@admin.com')
    teacher_1 = user_1.teacher

    print ('\n------------------------')
    print ('Creating Disciplines...')
    print ('------------------------\n')

    discipline_1 = Discipline.objects.create(name='Matemática')

    print ('\n------------------------')
    print ('Creating Disciplines...')
    print ('------------------------\n')

    school_1 = School.objects.create(name='CCI')


    print ('\n------------------------')
    print ('Creating School Levels...')
    print ('------------------------\n')

    school_level_1 = SchoolLevel.objects.create(
        name='1 série EM'
    )


    print ('\n------------------------')
    print ('Creating School Classes...')
    print ('------------------------\n')


    school_class_1 = SchoolClass.objects.create(
        school_level=school_level_1,
        year=2020,
        teacher=teacher_1,
        discipline=discipline_1,
        school=school_1,
        password='123'
    )

    print ('\n------------------------')
    print ('Creating Students ...')
    print ('------------------------\n')

    user_2 = create_user('Aninha', 'aninha@email.com')

    student_1 = user_2.student
    student_1.school_classes.add(school_class_1)
    
    print ('\n------------------------')
    print ('Creating Quiz ...')
    print ('------------------------\n')

    quiz_1 = Quiz.objects.create(
        title='Matriz',
        question='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget ligula eu lectus '
                 'lobortis condimentum. Aliquam nonummy auctor massa. Pellentesque habitant morbi tristique '
                 'senectus et netus et malesuada fames ac turpis egestas. Nulla at risus. '
                 'Quisque purus magna, auctor et, sagittis ac, posuere eu, lectus. Nam mattis, felis ut '
                 'adipiscing.',
        teacher=teacher_1
    )
    
    quiz_2 = Quiz.objects.create(
        title='Algebra',
        question='Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam eget ligula eu lectus '
                 'lobortis condimentum. Aliquam nonummy auctor massa. Pellentesque habitant morbi tristique '
                 'senectus et netus et malesuada fames ac turpis egestas. Nulla at risus. '
                 'Quisque purus magna, auctor et, sagittis ac, posuere eu, lectus. Nam mattis, felis ut '
                 'adipiscing.',
        teacher=teacher_1
    )


    print ('\n------------------------')
    print ('Creating Alternatives ...')
    print ('------------------------\n')

    alternative_1 = Alternative.objects.create(
        text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
             'tempor incididunt ut labore et d',
        is_answer=False,
        quiz=quiz_1,
        letter='A',
    )

    alternative_2 = Alternative.objects.create(
        text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
             'tempor incididunt ut labore et d',
        is_answer=False,
        quiz=quiz_1,
        letter='B',
    )

    alternative_3 = Alternative.objects.create(
        text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
             'tempor incididunt ut labore et d',
        is_answer=False,
        quiz=quiz_1,
        letter='C',
    )

    alternative_4 = Alternative.objects.create(
        text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
             'tempor incididunt ut labore et d',
        is_answer=True,
        quiz=quiz_1,
        letter='D',
    )


    alternative_5 = Alternative.objects.create(
        text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
             'tempor incididunt ut labore et d',
        is_answer=False,
        quiz=quiz_2,
        letter='A',
    )

    alternative_6 = Alternative.objects.create(
        text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
             'tempor incididunt ut labore et d',
        is_answer=False,
        quiz=quiz_2,
        letter='B',
    )

    alternative_7 = Alternative.objects.create(
        text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
             'tempor incididunt ut labore et d',
        is_answer=True,
        quiz=quiz_2,
        letter='C',
    )

    alternative_8 = Alternative.objects.create(
        text='Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod '
             'tempor incididunt ut labore et d',
        is_answer=False,
        quiz=quiz_2,
        letter='D',
    )

    print ('\n------------------------')
    print ('Creating Questionnaires ...')
    print ('------------------------\n')

    questionnaire_1 = Questionnaire.objects.create(
        title='Lista 1',
        start_date=datetime.datetime.strptime("2020-01-01 15:26", "%Y-%m-%d %H:%M"),
        due_date=datetime.datetime.strptime("2020-12-01 15:26", "%Y-%m-%d %H:%M"),
    )
    questionnaire_1.school_classes.add(school_class_1)
    questionnaire_1.save()
    questionnaire_1.quizzes.add(quiz_1)
    questionnaire_1.quizzes.add(quiz_2)
    questionnaire_1.save()

    questionnaire_2 = Questionnaire.objects.create(
        title='Lista 2',
        start_date=datetime.datetime.strptime("2020-01-01 15:26", "%Y-%m-%d %H:%M"),
        due_date=datetime.datetime.strptime("2020-12-01 15:26", "%Y-%m-%d %H:%M"),
    )
    questionnaire_2.school_classes.add(school_class_1)
    questionnaire_2.save()
    questionnaire_2.quizzes.add(quiz_1)
    questionnaire_2.quizzes.add(quiz_2)
    questionnaire_2.save()




import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chausant.settings')
django.setup()

from questionnaire.models import Teacher
from questionnaire.models import Discipline
from questionnaire.models import SchoolLevel
from questionnaire.models import SchoolClass
from questionnaire.models import Student
from questionnaire.models import Questionnaire
from questionnaire.models import Quiz
from questionnaire.models import Alternative
from questionnaire.models import User
from questionnaire.models import School

from django.core.exceptions import ValidationError
from django.db import IntegrityError

populate()