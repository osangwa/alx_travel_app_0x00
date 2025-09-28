# ALX Travel App

A Django-based travel booking application with listings, bookings, and reviews.

## Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run migrations: `python manage.py migrate`
6. Seed the database: `python manage.py seed`

## Models

- **Listing**: Properties available for booking
- **Booking**: Reservations made by users
- **Review**: User reviews and ratings for listings

## Seeding

The application includes a management command to populate the database with sample data:

```bash
python manage.py seed
This will create:

4 sample users

3 sample listings

Multiple bookings

Reviews for listings
