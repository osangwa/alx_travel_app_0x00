import os
import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from listings.models import Listing, Booking, Review
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Seed the database with sample data for listings, bookings, and reviews'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')
        
        # Create sample users if they don't exist
        users = self.create_sample_users()
        
        # Create sample listings
        listings = self.create_sample_listings(users)
        
        # Create sample bookings
        bookings = self.create_sample_bookings(listings, users)
        
        # Create sample reviews
        self.create_sample_reviews(listings, users, bookings)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully seeded database with {len(users)} users, '
                f'{len(listings)} listings, {len(bookings)} bookings, and reviews'
            )
        )

    def create_sample_users(self):
        users_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'mike_wilson', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Wilson'},
            {'username': 'sarah_jones', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Jones'},
        ]
        
        users = []
        for user_data in users_data:
            user, created = User.objects.get_or_create(
                username=user_data['username'],
                defaults=user_data
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f'Created user: {user.username}')
            users.append(user)
        
        return users

    def create_sample_listings(self, users):
        listings_data = [
            {
                'title': 'Cozy Downtown Apartment',
                'description': 'A beautiful apartment in the heart of downtown with amazing city views.',
                'address': '123 Main St, Downtown, City',
                'property_type': 'apartment',
                'price_per_night': 120.00,
                'max_guests': 4,
                'bedrooms': 2,
                'bathrooms': 1,
                'amenities': 'WiFi,Kitchen,Air Conditioning,TV',
                'host': users[0],
            },
            {
                'title': 'Luxury Beach Villa',
                'description': 'Stunning beachfront villa with private pool and direct beach access.',
                'address': '456 Beach Rd, Coastal Area',
                'property_type': 'villa',
                'price_per_night': 350.00,
                'max_guests': 8,
                'bedrooms': 4,
                'bathrooms': 3,
                'amenities': 'Pool,WiFi,Kitchen,Air Conditioning,TV,Garden',
                'host': users[1],
            },
            {
                'title': 'Mountain Cabin Retreat',
                'description': 'Peaceful cabin in the mountains perfect for nature lovers.',
                'address': '789 Mountain View, Forest Area',
                'property_type': 'cabin',
                'price_per_night': 95.00,
                'max_guests': 6,
                'bedrooms': 3,
                'bathrooms': 2,
                'amenities': 'Fireplace,WiFi,Kitchen,Garden',
                'host': users[2],
            },
        ]
        
        listings = []
        for listing_data in listings_data:
            listing, created = Listing.objects.get_or_create(
                title=listing_data['title'],
                defaults=listing_data
            )
            if created:
                self.stdout.write(f'Created listing: {listing.title}')
            listings.append(listing)
        
        return listings

    def create_sample_bookings(self, listings, users):
        bookings = []
        
        # Create some past bookings
        for i, listing in enumerate(listings):
            check_in = datetime.now().date() - timedelta(days=30 + i*7)
            check_out = check_in + timedelta(days=3 + i)
            
            booking = Booking.objects.create(
                listing=listing,
                user=users[(i + 1) % len(users)],  # Use different user than host
                check_in=check_in,
                check_out=check_out,
                total_price=listing.price_per_night * (check_out - check_in).days,
                guests=random.randint(1, listing.max_guests),
                status='completed',
            )
            bookings.append(booking)
            self.stdout.write(f'Created booking: {booking.booking_id}')
        
        return bookings

    def create_sample_reviews(self, listings, users, bookings):
        review_texts = [
            "Amazing place! Would definitely stay again.",
            "Great location and very comfortable.",
            "Nice property but could use some updates.",
            "Perfect for our family vacation!",
            "Beautiful views and excellent amenities.",
        ]
        
        for i, listing in enumerate(listings):
            # Create 1-2 reviews per listing
            for j in range(random.randint(1, 2)):
                review_user = users[(i + j) % len(users)]
                
                # Check if this user has already reviewed this listing
                if not Review.objects.filter(listing=listing, user=review_user).exists():
                    review = Review.objects.create(
                        listing=listing,
                        user=review_user,
                        rating=random.randint(3, 5),  # Ratings between 3-5
                        comment=random.choice(review_texts),
                    )
                    self.stdout.write(f'Created review: {review.review_id}')
