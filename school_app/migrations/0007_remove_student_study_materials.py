# Generated by Django 4.2.5 on 2023-11-20 06:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('school_app', '0006_student_study_materials'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='study_materials',
        ),
    ]
