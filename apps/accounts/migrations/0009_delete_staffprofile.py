# Generated by Django 4.2.10 on 2025-06-21 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_studentprofile_room'),
    ]

    operations = [
        migrations.DeleteModel(
            name='StaffProfile',
        ),
    ]
