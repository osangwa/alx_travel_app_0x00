from django.test import TestCase
from django.contrib.auth.models import User
from .models import Listing

class ListingModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        
    def test_listing_creation(self):
        listing = Listing.objects.create(
            title='Test Listing',
            description='Test Description',
            address='Test Address',
            property_type='apartment',
            price_per_night=100.00,
            max_guests=4,
            bedrooms=2,
            bathrooms=1,
            host=self.user
        )
        self.assertEqual(str(listing), 'Test Listing - apartment')
