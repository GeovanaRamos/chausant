from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
	full_name = models.CharField(max_length=70)
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
		return self.full_name

class Discipline(models.Model):
	name = models.CharField(max_length=50)

	class Meta:
		verbose_name = "Disciplina"
		verbose_name_plural = "Disciplina"

	def __str__(self):
		return self.name

class SchoolLevel(models.Model):
	number = models.IntegerField()
	level = models.CharField(max_length=20)

	class Meta:
		verbose_name = "Série Escolar"
		verbose_name_plural = "Séries Escolares"

	def __str__(self):
		return str(self.number) + '°' + ' ano ' + self.level

class SchoolClass(models.Model):

	school_level = models.ForeignKey(SchoolLevel, on_delete=models.CASCADE)
	year = models.IntegerField()
	letter = models.CharField(max_length=1, blank=True)
	teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
	discipline = models.ForeignKey(Discipline, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Turma"
		verbose_name_plural = "Turmas"

	def __str__(self):
		school_class =  "Turma " + self.letter + '/' + str(self.year) + '-' + str(self.discipline)
		return  str(self.school_level) + school_class


class Student(models.Model):

	school_classes = models.ManyToManyField(SchoolClass, blank=True)
	user = models.OneToOneField(User, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Estudante"
		verbose_name_plural = "Estudantes"

	def __str__(self):
		return self.full_name

class Quiz(models.Model):

	title = models.CharField(max_length=50)
	question = models.TextField()
	
	class Meta:
		verbose_name = "Questão"
		verbose_name_plural = "Questões"

	def __str__(self):
		return self.title

class Questionnaire(models.Model):

	title = models.CharField(max_length=50)
	school_classes = models.ManyToManyField(SchoolClass)
	start_date = models.DateTimeField( auto_now=False, auto_now_add=False)
	due_date = models.DateTimeField( auto_now=False, auto_now_add=False)
	is_suspended = models.BooleanField(default=False)
	quizzes = models.ManyToManyField(Quiz, blank=True)

	class Meta:
		verbose_name = "Lista de Exercícios"
		verbose_name_plural = "Listas de Exercícios"

	def __str__(self):
		return self.title

class Alternative(models.Model):

	text = models.CharField(max_length=20, help_text="Digite o texto da alternativa.")
	is_answer = models.BooleanField(default=False)
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	letter = models.CharField(max_length=1)

	class Meta:
		verbose_name = "Alternativa"
		verbose_name_plural = "Alternativas"

	def __str__(self):
		return self.letter


class QuizGrade(models.Model):

	grade = models.FloatField()
	quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
	student = models.ForeignKey(Student, on_delete=models.CASCADE)

	class Meta:
		verbose_name = "Notas"
		verbose_name_plural = "Notas"

	def __str__(self):
		return "Nota" + self.quiz.title

