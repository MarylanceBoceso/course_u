# Generated by Django 4.2.4 on 2023-12-13 04:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='QuestionSet',
            fields=[
                ('set_id', models.AutoField(primary_key=True, serialize=False)),
                ('n_questions', models.IntegerField()),
                ('is_completed', models.BooleanField(default=False)),
                ('score', models.IntegerField(default=0)),
                ('year', models.PositiveIntegerField(default=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'year')},
            },
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('question_id', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('question', models.CharField(max_length=1000)),
                ('description', models.CharField(max_length=1000)),
                ('options', models.JSONField()),
                ('correct_option', models.IntegerField()),
                ('field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.field')),
                ('skills', models.ManyToManyField(to='website.skill')),
            ],
        ),
        migrations.CreateModel(
            name='UserResponse',
            fields=[
                ('response', models.AutoField(auto_created=True, primary_key=True, serialize=False)),
                ('selected_option', models.IntegerField(blank=True, null=True)),
                ('is_correct', models.BooleanField(blank=True, null=True)),
                ('is_answered', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='assessment.test')),
                ('set', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='assessment.questionset')),
            ],
            options={
                'unique_together': {('question', 'set')},
            },
        ),
    ]
