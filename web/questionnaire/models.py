from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('É preciso informar um email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('request_type', 0)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):

    TEACHER = 0
    STUDENT = 1

    USER_TYPES = (
        (TEACHER, "Professor"),
        (STUDENT, "Aluno"),
    )

    username = None
    email = models.EmailField(verbose_name="Email", unique=True)
    full_name = models.CharField(verbose_name="Nome Completo", max_length=70)
    request_type = models.IntegerField(verbose_name="Tipo de Usuário", choices=USER_TYPES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"

    def __str__(self):
        return self.full_name

    def get_classes(self):
        if hasattr(self, 'student'):
            return self.student.get_classes()
        elif hasattr(self, 'teacher'):
            return self.teacher.get_classes()
        else:
            return SchoolClass.objects.none()


@receiver(post_save, sender=User)
def update_user_type(sender, instance, created, **kwargs):
    if created:
        if instance.request_type == User.TEACHER:
            Teacher.objects.create(user=instance)
        elif instance.request_type == User.STUDENT:
            Student.objects.create(user=instance)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Professor"
        verbose_name_plural = "Professores"

    def __str__(self):
        return self.user.full_name

    def get_classes(self):
        return SchoolClass.objects.filter(teacher=self)


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
    school_level = models.ForeignKey(verbose_name="Nível Escolar", to=SchoolLevel, on_delete=models.PROTECT)
    school = models.ForeignKey(School, verbose_name="Escola", on_delete=models.PROTECT)
    year = models.IntegerField(verbose_name="Ano de Realização")
    teacher = models.ForeignKey(verbose_name="Professor", to=Teacher, on_delete=models.PROTECT)
    discipline = models.ForeignKey(verbose_name="Disciplina", to=Discipline, on_delete=models.PROTECT)
    password = models.CharField(max_length=50)

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

    def get_classes(self):
        return self.school_classes.all()


class Quiz(models.Model):
    title = models.CharField(verbose_name="Título", max_length=50)
    question = models.TextField(verbose_name="Pergunta")
    teacher = models.ForeignKey(verbose_name="Professor", to=Teacher, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Questão"
        verbose_name_plural = "Questões"

    def __str__(self):
        return self.title

    def is_in_questionnaire(self):
        if Questionnaire.objects.filter(quizzes__pk=self.pk).exists():
            return True
        return False


class Questionnaire(models.Model):
    title = models.CharField(verbose_name="Título", max_length=50)
    school_classes = models.ManyToManyField(verbose_name="Turmas", to=SchoolClass)
    start_date = models.DateTimeField(verbose_name="Início", auto_now=False, auto_now_add=False)
    due_date = models.DateTimeField(verbose_name="Término", auto_now=False, auto_now_add=False)
    quizzes = models.ManyToManyField(verbose_name="Questões", to=Quiz, blank=True)

    class Meta:
        verbose_name = "Lista de Exercícios"
        verbose_name_plural = "Listas de Exercícios"

    def __str__(self):
        return self.title

    def is_active(self):
        now = timezone.now()
        return self.start_date <= now <= self.due_date

    def student_has_concluded(self, student):
        if QuestionnaireConclusion.objects.filter(questionnaire=self, student=student).exists():
            return True

        return False


class Alternative(models.Model):
    text = models.CharField(verbose_name="Texto", max_length=500)
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
        return self.questionnaire + " " + "Nota " + self.quiz.title + " " + self.student


class QuestionnaireConclusion(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    questionnaire = models.ForeignKey(Questionnaire, on_delete=models.CASCADE)
    concluded_at = models.DateTimeField(verbose_name="Data de Conclusão da Lista",
                                        auto_now=False, auto_now_add=False, editable=False)

    def get_hit_percentage(self):
        count = 0
        correct = 0

        for quiz in self.questionnaire.quizzes.all():
            if QuizResult.objects.get(quiz=quiz, student=self.student,
                                      questionnaire=self.questionnaire).is_correct:
                correct += 1

            count += 1

        return correct * 100 / count

    def save(self, *args, **kwargs):
        if not self.id:
            self.concluded_at = timezone.now()
        return super(QuestionnaireConclusion, self).save(*args, **kwargs)

