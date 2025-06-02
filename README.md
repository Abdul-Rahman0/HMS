# Hostel Management System

A comprehensive hostel management system built with Django and PostgreSQL, featuring role-based access control, room management, booking system, payment processing, and maintenance tracking.

## Features

- Multi-role authentication (Admin, Student, Receptionist, Maintenance Staff)
- Student registration and hostel application workflow
- Room management and allocation
- Booking and check-in/check-out system
- Payment management with receipt generation
- Maintenance request tracking
- Reports and analytics dashboard
- Email notifications
- System settings management

## Technology Stack

- Django 4.2.7
- PostgreSQL
- Bootstrap 5 (White and Light Green Theme)
- Django REST Framework
- Celery for background tasks
- Redis for caching

## Prerequisites

- Python 3.8+
- PostgreSQL
- Redis (for background tasks)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd hostel-management-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=postgres://user:password@localhost:5432/hostel_db
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

5. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create a superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

```
hostel/
├── apps/
│   ├── accounts/        # User authentication and profiles
│   ├── rooms/          # Room management
│   ├── bookings/       # Booking system
│   ├── payments/       # Payment processing
│   ├── maintenance/    # Maintenance requests
│   └── reports/        # Reports and analytics
├── static/             # Static files
├── templates/          # HTML templates
├── media/             # User-uploaded files
└── config/            # Project settings
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 