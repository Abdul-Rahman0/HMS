from django.db import migrations

def create_initial_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    roles = [
        {'name': 'admin', 'description': 'System administrator'},
        {'name': 'student', 'description': 'Student living in the hostel'},
        {'name': 'receptionist', 'description': 'Receptionist managing check-ins and check-outs'},
        {'name': 'maintenance', 'description': 'Maintenance staff handling repairs and maintenance'},
        {'name': 'housekeeping', 'description': 'Housekeeping staff managing cleaning and supplies'},
    ]
    for role_data in roles:
        Role.objects.get_or_create(
            name=role_data['name'],
            defaults={'description': role_data['description']}
        )

def remove_initial_roles(apps, schema_editor):
    Role = apps.get_model('accounts', 'Role')
    Role.objects.filter(name__in=['admin', 'student', 'receptionist', 'maintenance', 'housekeeping']).delete()

class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]
    operations = [
        migrations.RunPython(create_initial_roles, remove_initial_roles),
    ] 