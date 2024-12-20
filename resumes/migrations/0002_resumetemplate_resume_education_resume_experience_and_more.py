# Generated by Django 5.1.2 on 2024-10-22 18:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resumes', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('template_file', models.FileField(upload_to='templates/')),
            ],
        ),
        migrations.AddField(
            model_name='resume',
            name='education',
            field=models.TextField(default='No education listed.'),
        ),
        migrations.AddField(
            model_name='resume',
            name='experience',
            field=models.TextField(default='No experience listed.'),
        ),
        migrations.AddField(
            model_name='resume',
            name='skills',
            field=models.TextField(default='No skills listed.'),
        ),
        migrations.AddField(
            model_name='resume',
            name='summary',
            field=models.TextField(default='Summary not provided.'),
        ),
        migrations.AlterField(
            model_name='resume',
            name='title',
            field=models.CharField(default='Untitled Resume', max_length=200),
        ),
        migrations.AlterField(
            model_name='resume',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('github_url', models.URLField(blank=True, null=True)),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projects', to='resumes.resume')),
            ],
        ),
        migrations.CreateModel(
            name='ResumeDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf_file', models.FileField(upload_to='resume/')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='resumes.resume')),
            ],
        ),
        migrations.AddField(
            model_name='resume',
            name='template',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='resumes.resumetemplate'),
        ),
        migrations.DeleteModel(
            name='Section',
        ),
    ]
