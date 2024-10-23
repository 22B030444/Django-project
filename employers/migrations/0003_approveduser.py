# Generated by Django 5.0.4 on 2024-10-22 21:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employers', '0002_employer_user'),
        ('resumes', '0003_resume_approved'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApprovedUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approval_date', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='approved_users', to='employers.employer')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resumes.resume')),
            ],
        ),
    ]