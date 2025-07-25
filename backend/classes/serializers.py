from rest_framework import serializers
from .models import FitnessClass, ClassBooking

class FitnessClassSerializer(serializers.ModelSerializer):
    instructor_name = serializers.CharField(source='instructor.username', read_only=True)
    available_spots = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = FitnessClass
        fields = ['id', 'name', 'description', 'instructor', 'instructor_name',
                 'datetime', 'duration_minutes', 'capacity', 'available_spots',
                 'is_full', 'required_membership_tier', 'price', 'is_active']

class ClassBookingSerializer(serializers.ModelSerializer):
    class_details = FitnessClassSerializer(source='fitness_class', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ClassBooking
        fields = ['id', 'fitness_class', 'class_details', 'user', 'user_name',
                 'booking_date', 'status', 'notes']
        read_only_fields = ['booking_date']