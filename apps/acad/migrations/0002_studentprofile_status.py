# Generated by Django 4.2.4 on 2023-12-25 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acad', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='status',
            field=models.CharField(blank=True, default='enrolled', max_length=255, null=True),
        ),
    ]
