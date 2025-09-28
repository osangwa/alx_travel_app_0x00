from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking, Review


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Review
        fields = ['review_id', 'user', 'rating', 'comment', 'created_at']
        read_only_fields = ['review_id', 'created_at']


class ListingSerializer(serializers.ModelSerializer):
    host = UserSerializer(read_only=True)
    reviews = ReviewSerializer(many=True, read_only=True)
    average_rating = serializers.SerializerMethodField()
    
    class Meta:
        model = Listing
        fields = [
            'listing_id', 'title', 'description', 'address', 'property_type',
            'price_per_night', 'max_guests', 'bedrooms', 'bathrooms', 'amenities',
            'host', 'is_active', 'average_rating', 'reviews', 'created_at'
        ]
        read_only_fields = ['listing_id', 'created_at', 'average_rating']
    
    def get_average_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class BookingSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.UUIDField(write_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'booking_id', 'listing', 'listing_id', 'user', 'check_in', 'check_out',
            'total_price', 'guests', 'status', 'special_requests', 'created_at'
        ]
        read_only_fields = ['booking_id', 'created_at']
    
    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        return data


class BookingCreateSerializer(serializers.ModelSerializer):
    listing_id = serializers.UUIDField()
    
    class Meta:
        model = Booking
        fields = ['listing_id', 'check_in', 'check_out', 'guests', 'special_requests']
    
    def validate(self, data):
        if data['check_in'] >= data['check_out']:
            raise serializers.ValidationError("Check-out date must be after check-in date")
        return data
