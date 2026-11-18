# ANO KAYA 'TO?

## Project Overview
ANO KAYA 'TO? is a Filipino dream journal application designed to help users record their dreams, explore dream symbols, and discover traditional Filipino *pamahiin* interpretations.

## Technologies Used
- Python
- Django
- Django Templates (HTML)
- PostgreSQL
- Supabase
- Git and GitHub

## Account Feature

The current development includes:

- User registration
- User login and logout
- Password hashing through Django authentication
- Role-based access (Admin and User)
- Separate dashboards for Admin and User
- User profile viewing and editing
- PostgreSQL database integration through Supabase

## Project Structure

- `accounts/` – Account application, models, forms, views, URLs, and templates
- `config/` – Django project settings and configuration
- `manage.py` – Django management utility
- `requirements.txt` – Project dependencies

## Setup Instructions

1. Clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

   `pip install -r requirements.txt`

4. Create a `.env` file containing the required Django and Supabase PostgreSQL environment variables.
5. Apply migrations:

   `python manage.py migrate`

6. Start the development server:

   `python manage.py runserver`

## Developers
Christian Josh Sapuras – G7