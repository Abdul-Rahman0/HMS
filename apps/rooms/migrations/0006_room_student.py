# Generated by Django 4.2.10 on 2025-06-14 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_remove_studentprofile_room'),
        ('rooms', '0005_alter_guestlog_check_in_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='student',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.studentprofile'),
        ),
    ]
