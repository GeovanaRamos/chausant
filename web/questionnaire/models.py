from django.db import models

class Questionnarie(models.Model):

	password = models.CharField(max_length=20, help_text='Insira a senha do questionário.')

	class Meta:
		verbose_name = 'Questionnarie'

	def __str__(self):
		return self.name

class Quiz(models.Model):

	question = models.CharField(max_length=500, help_text='Digite o texto da pergunta.')
	questionnarie = models.ManyToManyField(Questionnarie)
	
	class Meta:
		verbose_name = 'Quiz'

	def __str__(self):
		return self.name

class Alternative(models.Model):

	text = models.CharField(max_length=20, help_text='Digite o texto da alternativa.')
	is_answer = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Alternative'

	def __str__(self):
		return self.name