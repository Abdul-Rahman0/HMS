# Generated by Django 4.2.10 on 2025-06-14 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_studentprofile_student_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='room',
        ),
    ]
