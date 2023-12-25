
# Generated by Django 4.2.4 on 2023-12-25 12:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('acad', '0002_studentprofile_status'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('specialization', models.CharField(max_length=255, verbose_name='1. What specialization did you graduate with?')),
                ('employed', models.BooleanField(default=False, verbose_name='2. Are you currently employed?')),
                ('current_job_title', models.CharField(blank=True, max_length=255, verbose_name='3. If yes, what is your current job title')),
                ('received_recommendation', models.BooleanField(default=False, verbose_name='4. In your 4th year, did you receive a recommended specialization from the system?')),
                ('confidence_rating', models.CharField(blank=True, choices=[('Very confident', 'Very confident'), ('Moderately confident', 'Moderately confident'), ('Somewhat confident', 'Somewhat confident'), ('Not confident at all', 'Not confident at all')], max_length=255, verbose_name='5. If yes, how confident were you about the recommended specialization at the time?')),
                ('recommendation_influence', models.CharField(blank=True, choices=[('Significantly', 'Significantly'), ('Moderately', 'Moderately'), ('Slightly', 'Slightly'), ('Not at all', 'Not at all')], max_length=255, verbose_name='6. Did the recommended specialization influence your decision to choose your current field of study?')),
                ('recommendation_influence_reason', models.TextField(blank=True, verbose_name='7. Why or why not did the recommended specialization influence your decision?')),
                ('system_information_helpfulness', models.CharField(blank=True, choices=[('Very helpful', 'Very helpful'), ('Moderately helpful', 'Moderately helpful'), ('Somewhat helpful', 'Somewhat helpful'), ('Not helpful at all', 'Not helpful at all')], max_length=255, verbose_name='8. How helpful was the information provided by the recommendation system in understanding your potential career paths?')),
                ('recommendation_system_improvements', models.TextField(blank=True, verbose_name='9. Please share any specific improvements you suggest for the recommendation system.')),
                ('job_alignment', models.CharField(blank=True, choices=[('Very aligned', 'Very aligned'), ('Moderately aligned', 'Moderately aligned'), ('Somewhat aligned', 'Somewhat aligned'), ('Not at all aligned', 'Not at all aligned')], max_length=255, verbose_name='10. Do you consider your current job aligned with the recommended specialization?')),
                ('job_misalignment_reason', models.TextField(blank=True, verbose_name='11. If your current job is not aligned with the recommended specialization, why not?')),
                ('job_satisfaction', models.CharField(blank=True, choices=[('Very satisfied', 'Very satisfied'), ('Satisfied', 'Satisfied'), ('Neutral', 'Neutral'), ('Dissatisfied', 'Dissatisfied'), ('Very dissatisfied', 'Very dissatisfied')], max_length=255, verbose_name='12. How satisfied are you with your current job overall?')),
                ('study_preparation', models.CharField(blank=True, choices=[('Very well', 'Very well'), ('Moderately', 'Moderately'), ('Somewhat', 'Somewhat'), ('Not well at all', 'Not well at all')], max_length=255, verbose_name='13. How well do your skills and knowledge acquired during your studies prepare you for your current job?')),
                ('explored_learning_materials', models.BooleanField(default=False, verbose_name='14. Did you explore any of the recommended learning materials (courses, articles, etc.) provided by the system?')),
                ('material_satisfaction', models.CharField(blank=True, choices=[('Very satisfied', 'Very satisfied'), ('Moderately satisfied', 'Moderately satisfied'), ('Somewhat satisfied', 'Somewhat satisfied'), ('Not satisfied at all', 'Not satisfied at all')], max_length=255, verbose_name='15. How satisfied were you with the quality and relevance of the provided learning materials?')),
                ('material_skill_gain', models.CharField(blank=True, choices=[('Significantly', 'Significantly'), ('Moderately', 'Moderately'), ('Slightly', 'Slightly'), ('Not at all', 'Not at all')], max_length=255, verbose_name='16. Did the learning materials provided by the system help you gain new skills or knowledge relevant to your chosen field?')),
                ('accessed_job_postings', models.BooleanField(default=False, verbose_name='17. Did you access any of the job postings recommended by the system?')),
                ('posting_job_understanding', models.CharField(blank=True, choices=[('Very helpful', 'Very helpful'), ('Moderately helpful', 'Moderately helpful'), ('Somewhat helpful', 'Somewhat helpful'), ('Not helpful at all', 'Not helpful at all')], max_length=255, verbose_name='18. If yes, how helpful were the job postings in understanding the types of jobs available in your field?')),
                ('posting_career_influence', models.CharField(blank=True, choices=[('Significantly', 'Significantly'), ('Moderately', 'Moderately'), ('Slightly', 'Slightly'), ('Not at all', 'Not at all')], max_length=255, verbose_name='19. Did the job postings provided by the system influence your job search process or career goals?')),
                ('more_specialized_postings', models.BooleanField(default=False, verbose_name='20. Would you like to see more specialized job postings tailored to your specific skillset or interests?')),
                ('additional_feedback', models.TextField(blank=True, verbose_name='21. Please share any other thoughts or feedback you have about the specialization recommendation system or your career journey.')),
                ('timestamp', models.DateField(auto_now_add=True)),
                ('academic_course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='acad.course')),
                ('user', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='surveys', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
