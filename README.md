# News Application

## Project Description
A Django-based news application supporting readers, editors, journalists, publishers, articles, newsletters, and a REST API.

## Technologies
- Python 3.13
- Django
- Django REST Framework
- MariaDB
- mysqlclient

## Installation
1. Install Python and MariaDB.
2. Open the project folder in the terminal.
3. Install dependencies:

   pip install -r requirements.txt

4. Configure your MariaDB credentials in news_project/settings.py.
5. Apply database migrations:

   python manage.py migrate

## Run the Application
Run:

    python manage.py runserver

Open http://127.0.0.1:8000/ in your browser.

## Run Tests
Run:

    python manage.py test news

## Project Structure
- news/ - Models, views, serializers, API endpoints, tests, and templates.
- news_project/ - Django settings and URL configuration.
- manage.py - Django management commands.
- requirements.txt - Python dependencies.

## Database
The application is configured to use MariaDB. Keep database credentials private and never commit passwords to a public repository.
