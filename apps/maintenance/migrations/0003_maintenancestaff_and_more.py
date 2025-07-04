# Generated by Django 4.2.10 on 2025-06-06 13:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maintenance', '0002_alter_maintenancerequest_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaintenanceStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='maintenancecomment',
            name='maintenance_request',
        ),
        migrations.RemoveField(
            model_name='maintenancecomment',
            name='user',
        ),
        migrations.RemoveField(
            model_name='maintenancerequest',
            name='room',
        ),
        migrations.RemoveField(
            model_name='maintenancerequest',
            name='submitted_by',
        ),
        migrations.DeleteModel(
            name='MaintenanceAttachment',
        ),
        migrations.DeleteModel(
            name='MaintenanceComment',
        ),
        migrations.DeleteModel(
            name='MaintenanceRequest',
        ),
    ]
