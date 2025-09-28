from django.contrib import admin
from .models import Listing, Booking, Review

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'price_per_night', 'host', 'is_active']
    list_filter = ['property_type', 'is_active']

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'listing', 'user', 'check_in', 'check_out', 'status']
    list_filter = ['status']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'listing', 'user', 'rating', 'created_at']
    list_filter = ['rating']
