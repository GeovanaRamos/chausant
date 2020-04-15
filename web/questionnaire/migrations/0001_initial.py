# Generated by Django 2.2.12 on 2020-04-15 21:32

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Email')),
                ('full_name', models.CharField(max_length=70, verbose_name='Nome Completo')),
                ('request_type', models.IntegerField(choices=[(0, 'Professor'), (1, 'Aluno')], verbose_name='Tipo de Usuário')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Usuário',
                'verbose_name_plural': 'Usuários',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Discipline',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nome')),
            ],
            options={
                'verbose_name': 'Disciplina',
                'verbose_name_plural': 'Disciplina',
            },
        ),
        migrations.CreateModel(
            name='Questionnaire',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Título')),
                ('start_date', models.DateTimeField(verbose_name='Início')),
                ('due_date', models.DateTimeField(verbose_name='Término')),
                ('is_suspended', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'Lista de Exercícios',
                'verbose_name_plural': 'Listas de Exercícios',
            },
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Título')),
                ('question', models.TextField(verbose_name='Pergunta')),
            ],
            options={
                'verbose_name': 'Questão',
                'verbose_name_plural': 'Questões',
            },
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'Escola',
                'verbose_name_plural': 'Escolas',
            },
        ),
        migrations.CreateModel(
            name='SchoolClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField(verbose_name='Ano de Realização')),
                ('discipline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Discipline', verbose_name='Disciplina')),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.School', verbose_name='Escola')),
            ],
            options={
                'verbose_name': 'Turma',
                'verbose_name_plural': 'Turmas',
            },
        ),
        migrations.CreateModel(
            name='SchoolLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Nível Escolar',
                'verbose_name_plural': 'Níveis Escolares',
            },
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Professor',
                'verbose_name_plural': 'Professores',
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_classes', models.ManyToManyField(blank=True, to='questionnaire.SchoolClass')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Estudante',
                'verbose_name_plural': 'Estudantes',
            },
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='school_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.SchoolLevel', verbose_name='Nível Escolar'),
        ),
        migrations.AddField(
            model_name='schoolclass',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Teacher', verbose_name='Professor'),
        ),
        migrations.CreateModel(
            name='QuizResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_correct', models.BooleanField()),
                ('questionnaire', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Questionnaire')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Student')),
            ],
            options={
                'verbose_name': 'Notas',
                'verbose_name_plural': 'Notas',
            },
        ),
        migrations.AddField(
            model_name='quiz',
            name='teacher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Teacher', verbose_name='Professor'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='quizzes',
            field=models.ManyToManyField(blank=True, to='questionnaire.Quiz', verbose_name='Questões'),
        ),
        migrations.AddField(
            model_name='questionnaire',
            name='school_classes',
            field=models.ManyToManyField(to='questionnaire.SchoolClass', verbose_name='Turmas'),
        ),
        migrations.CreateModel(
            name='Alternative',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=20, verbose_name='Texto')),
                ('is_answer', models.BooleanField(default=False, verbose_name='É a correta?')),
                ('letter', models.CharField(max_length=1)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questionnaire.Quiz', verbose_name='Perguntas')),
            ],
            options={
                'verbose_name': 'Alternativa',
                'verbose_name_plural': 'Alternativas',
            },
        ),
    ]
