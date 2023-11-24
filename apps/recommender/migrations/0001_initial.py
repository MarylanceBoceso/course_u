# Generated by Django 4.2.7 on 2023-11-24 09:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField(default=0)),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='website.skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserSkillSource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_type', models.CharField(max_length=50)),
                ('source_id', models.PositiveIntegerField()),
                ('user_skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recommender.userskill')),
            ],
        ),
        migrations.CreateModel(
            name='UserRecommendations',
            fields=[
                ('recommendation_id', models.AutoField(primary_key=True, serialize=False)),
                ('score_1', models.FloatField(blank=True, null=True)),
                ('score_2', models.FloatField(blank=True, null=True)),
                ('score_3', models.FloatField(blank=True, null=True)),
                ('current_year', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('field_1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_1', to='website.field')),
                ('field_2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_2', to='website.field')),
                ('field_3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='field_3', to='website.field')),
                ('selected_field', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='website.field')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['user'],
                'unique_together': {('user', 'current_year')},
            },
        ),
    ]