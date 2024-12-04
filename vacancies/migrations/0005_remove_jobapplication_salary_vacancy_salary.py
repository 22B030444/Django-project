# Generated by Django 5.1.2 on 2024-12-04 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vacancies', '0004_jobapplication_salary'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplication',
            name='salary',
        ),
        migrations.AddField(
            model_name='vacancy',
            name='salary',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]
