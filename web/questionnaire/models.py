from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):

    TEACHER = 0
    STUDENT = 1

    USER_TYPES = (
        (TEACHER, "Professor"),
        (STUDENT, "Aluno"),
    )

    email = models.EmailField(verbose_name="Email", unique=True)
    full_name = models.CharField(verbose_name="Nome Completo", max_length=70)
    request_type = models.IntegerField(verbose_name="Tipo de Usuário", choices=USER_TYPES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

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
def update_stock(sender, instance, created, **kwargs):
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
    school_level = models.ForeignKey(verbose_name="Nível Escolar", to=SchoolLevel, on_delete=models.CASCADE)
    school = models.ForeignKey(School, verbose_name="Escola", on_delete=models.CASCADE)
    year = models.IntegerField(verbose_name="Ano de Realização")
    teacher = models.ForeignKey(verbose_name="Professor", to=Teacher, on_delete=models.CASCADE)
    discipline = models.ForeignKey(verbose_name="Disciplina", to=Discipline, on_delete=models.CASCADE)
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

    def get_concluding_students(self):
        questionnaire_conclusions = QuestionnaireConclusion.objects.filter(questionnaire=self)
        students = Student.objects.filter(pk__in=questionnaire_conclusions.values_list('student', flat=True))
        return students


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
        count, correct = 0

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

