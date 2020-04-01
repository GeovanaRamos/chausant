import os.path
import sys
import random
import string
import datetime

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))


def create_password():
    return '123abc'


def create_super_user(username, email):

    password = create_password()
    try:
        u = User.objects.create_superuser(username,
                                          email,
                                          password,
                                          is_validated=True)

        return u

    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")


def create_user(name, username, email):
    """
    Creates the user and ensures that if any error occurs the
    script does not continue
    """
    password = create_password()

    try:
        u = User.objects.create_user(
            full_name=name,
            username=username,
            email=email,
            password=password,
            is_validated=True
        )

        return u

    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")

def create_teacher(user):
    try:
        teacher = Teacher.objects.create(
            user=user
        )
        return teacher

    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")


def create_student(user, school_classes):
    try:
        student = Student.objects.create(user=user)
        for sc in school_classes:
            student.school_class.add(sc)
        student.save()
        return student
    except IntegrityError:
        raise ValidationError("An error occurred. Stopping the script")



def populate():
    print ('\n----------------------')
    print ('Populating Database...')
    print ('----------------------\n')

    create_super_user('admin', 'admin@admin.com')

    print ('\n------------------------')
    print ('Creating Disciplin...')
    print ('------------------------\n')

    discipline_1 = Discipline.objects.create(name='Matemática')

    print ('\n------------------------')
    print ('Creating Teachers...')
    print ('------------------------\n')

    user_1 = create_user('Ana', 'ana' ,'ana@email.com')
    user_2 = create_user('João', 'joao' ,'joao@email.com')

    teacher_1 = create_teacher(user_1)
    teacher_2 = create_teacher(user_2)


    print ('\n------------------------')
    print ('Creating School Levels...')
    print ('------------------------\n')

    school_level_1 = SchoolLevel.objects.create(
        number=9,
        level='EF'
    )
    school_level_2 = SchoolLevel.objects.create(
        number=1,
        level='EM'
    )
    school_level_3 = SchoolLevel.objects.create(
        number=2,
        level='EM'
    )

    print ('\n------------------------')
    print ('Creating School Classes...')
    print ('------------------------\n')


    school_class_1 = SchoolClass.objects.create(
        school_level=school_level_1,
        year=2020,
        letter='A',
        teacher=teacher_1,
        discipline=discipline_1,
    )

    school_class_2 = SchoolClass.objects.create(
        school_level=school_level_2,
        year=2020,
        teacher=teacher_2,
        discipline=discipline_1,
    )

    school_class_3 = SchoolClass.objects.create(
        school_level=school_level_3,
        year=2020,
        letter='A',
        teacher=teacher_2,
        discipline=discipline_1,
    )

    print ('\n------------------------')
    print ('Creating Students ...')
    print ('------------------------\n')

    user_3 = create_user('Aninha', 'aninha' ,'aninha@email.com')
    user_4 = create_user('Joãozinho', 'joaozinho' ,'joaozinho@email.com')

    student_1 = create_student(user_3, [school_class_1, school_class_2])
    student_2 = create_student(user_4, [school_class_2, school_class_3])
    
    print ('\n------------------------')
    print ('Creating Questionnaires ...')
    print ('------------------------\n')

    questionnaire_1 = Questionnaire.objects.create(
        title='Lista 1',
        start_date=datetime.datetime.strptime("2020-01-01 15:26", "%Y-%m-%d %H:%M"),
        due_date=datetime.datetime.strptime("2020-12-01 15:26", "%Y-%m-%d %H:%M"),
        is_suspended=False,
    )
    questionnaire_1.school_class.add(school_class_2)
    questionnaire_1.save()

    questionnaire_2 = Questionnaire.objects.create(
        title='Lista 2',
        start_date=datetime.datetime.strptime("2020-01-01 15:26", "%Y-%m-%d %H:%M"),
        due_date=datetime.datetime.strptime("2020-12-01 15:26", "%Y-%m-%d %H:%M"),
        is_suspended=False,
    )
    questionnaire_2.school_class.add(school_class_3)
    questionnaire_2.save()


    print ('\n------------------------')
    print ('Creating Quiz ...')
    print ('------------------------\n')

    quiz_1 = Quiz.objects.create(
        title='Matriz',
        question='Qual letra?',
    )
    quiz_1.questionnaire.add(questionnaire_1)
    quiz_1.save()
    
    quiz_2 = Quiz.objects.create(
        title='Algebra',
        question='Qual alternativa?',
    )
    quiz_2.questionnaire.add(questionnaire_2)
    quiz_2.save()

    print ('\n------------------------')
    print ('Creating Alternatives ...')
    print ('------------------------\n')

    alternative_1 = Alternative.objects.create(
        text='É A',
        is_answer=False,
        quiz=quiz_1,
        letter='A',
    )

    alternative_2 = Alternative.objects.create(
        text='É B',
        is_answer=False,
        quiz=quiz_1,
        letter='B',
    )

    alternative_3 = Alternative.objects.create(
        text='É C',
        is_answer=False,
        quiz=quiz_1,
        letter='C',
    )

    alternative_4 = Alternative.objects.create(
        text='É D',
        is_answer=True,
        quiz=quiz_1,
        letter='D',
    )


    alternative_5 = Alternative.objects.create(
        text='É A',
        is_answer=False,
        quiz=quiz_2,
        letter='A',
    )

    alternative_6 = Alternative.objects.create(
        text='É B',
        is_answer=False,
        quiz=quiz_2,
        letter='B',
    )

    alternative_7 = Alternative.objects.create(
        text='É C',
        is_answer=True,
        quiz=quiz_2,
        letter='C',
    )

    alternative_8 = Alternative.objects.create(
        text='É D',
        is_answer=False,
        quiz=quiz_2,
        letter='D',
    )


    print ('\n------------------------')
    print ('Creating QuizGrade ...')
    print ('------------------------\n')

    quiz_grade_1 = QuizGrade.objects.create(
        grade=80.20,
        quiz=quiz_1,
        student=student_1,
    )

    quiz_grade_2 = QuizGrade.objects.create(
        grade=50.20,
        quiz=quiz_2,
        student=student_2,
    )

    print ('\n------------------------------\n')
    print ('Database populated with sucess')
    print ('------------------------------\n')


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
from questionnaire.models import QuizGrade
from questionnaire.models import User

from django.core.exceptions import ValidationError
from django.db import IntegrityError

populate()