# Generated by Django 2.2.12 on 2020-04-17 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questionnaire', '0002_questionnaireconclusion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alternative',
            name='text',
            field=models.CharField(max_length=500, verbose_name='Texto'),
        ),
    ]