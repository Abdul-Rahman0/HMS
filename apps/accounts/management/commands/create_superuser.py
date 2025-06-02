from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.accounts.models import Role

User = get_user_model()

class Command(BaseCommand):
    help = 'Creates a superuser with admin role'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            # Create admin role if it doesn't exist
            admin_role, created = Role.objects.get_or_create(
                name='admin',
                defaults={'description': 'System administrator'}
            )
            
            # Create superuser
            User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='Admin@123',
                first_name='System',
                last_name='Administrator',
                role=admin_role
            )
            self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists')) 