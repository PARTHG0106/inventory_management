# Django Inventory Management System

A comprehensive inventory management system built with Django, featuring user authentication, product management, inventory tracking, sales and purchase orders, and more.

## Features

- User Authentication (Signup/Login/Logout)
- Role-based access control (Admin, Manager, Staff)
- Dashboard with analytics
- Product Management (CRUD)
- Supplier & Customer Management
- Inventory Tracking
- Sales & Purchase Orders
- Barcode/QR Code Integration
- Notifications
- Reporting Module
- REST API support
- Responsive UI with Bootstrap

## Setup Instructions

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and update the variables:
```bash
cp .env.example .env
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

7. For Celery worker (in a separate terminal):
```bash
celery -A inventory worker -l info
```

## Project Structure

```
inventory_management/
├── core/                 # Core app with shared functionality
├── users/               # User management app
├── products/            # Product management app
├── inventory/           # Inventory tracking app
├── suppliers/           # Supplier management app
├── customers/           # Customer management app
├── orders/              # Sales and purchase orders app
├── notifications/       # Notifications app
├── reports/             # Reporting app
└── api/                 # REST API app
```

## Development

- Use `python manage.py makemigrations` to create new migrations
- Use `python manage.py migrate` to apply migrations
- Use `python manage.py test` to run tests

## Deployment

The project is configured for deployment with:
- PostgreSQL database
- Gunicorn as WSGI server
- Whitenoise for static files
- Redis for Celery

## License

MIT License 