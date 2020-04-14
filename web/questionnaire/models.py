from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    full_name = models.CharField(verbose_name="Nome Completo", max_length=70)
    is_validated = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.full_name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.user.full_name


class Discipline(models.Model):
    name = models.CharField(verbose_name="Nome", max_length=50)

    class Meta:
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplina"

    def __str__(self):
        return self.name


class School(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Escola"
        verbose_name_plural = "Escolas"

    def __str__(self):
        return self.name


class SchoolLevel(models.Model):
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = "Nível Escolar"
        verbose_name_plural = "Níveis Escolares"

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    school_level = models.ForeignKey(verbose_name="Nível Escolar", to=SchoolLevel, on_delete=models.CASCADE)
    school = models.ForeignKey(School, verbose_name="Escola", on_delete=models.CASCADE)
    year = models.IntegerField(verbose_name="Ano de Realização")
    teacher = models.ForeignKey(verbose_name="Professor", to=Teacher, on_delete=models.CASCADE)
    discipline = models.ForeignKey(verbose_name="Disciplina", to=Discipline, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Turma"
        verbose_name_plural = "Turmas"

    def __str__(self):
        school_class = '/' + str(self.year) + ' - ' + str(self.discipline)
        return str(self.school_level) + school_class


class Student(models.Model):
    school_classes = models.ManyToManyField(SchoolClass, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"

    def __str__(self):
        return self.user.full_name


class Quiz(models.Model):
    title = models.CharField(verbose_name="Título", max_length=50)
    question = models.TextField(verbose_name="Pergunta")

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def __str__(self):
        return self.title


class Questionnaire(models.Model):
    title = models.CharField(verbose_name="Título", max_length=50)
    school_classes = models.ManyToManyField(verbose_name="Turmas", to=SchoolClass)
    start_date = models.DateTimeField(verbose_name="Início", auto_now=False, auto_now_add=False)
    due_date = models.DateTimeField(verbose_name="Término", auto_now=False, auto_now_add=False)
    is_suspended = models.BooleanField(default=False)
    quizzes = models.ManyToManyField(verbose_name="Questões", to=Quiz, blank=True)

    class Meta:
        verbose_name = "Lista de Exercícios"
        verbose_name_plural = "Listas de Exercícios"

    def __str__(self):
        return self.title

    def is_active(self):
        from django.utils import timezone
        now = timezone.now()
        return self.start_date <= now <= self.due_date


class Alternative(models.Model):
    text = models.CharField(verbose_name="Texto", max_length=20)
    is_answer = models.BooleanField(verbose_name="É a correta?", default=False)
    quiz = models.ForeignKey(verbose_name="Perguntas", to=Quiz, on_delete=models.CASCADE)
    letter = models.CharField(max_length=1)

    class Meta:
        verbose_name = "Alternativa"
        verbose_name_plural = "Alternativas"

    def __str__(self):
        return self.letter


class QuizResult(models.Model):
    is_correct = models.BooleanField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Notas"
        verbose_name_plural = "Notas"
        # TODO unique

    def __str__(self):
        return "Nota" + self.quiz.title
