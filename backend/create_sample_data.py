import os
import django
from datetime import datetime, timedelta
from django.utils import timezone

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from memberships.models import MembershipPlan, UserMembership
from workouts.models import Exercise, Workout, WorkoutExercise
from classes.models import FitnessClass

User = get_user_model()

def create_sample_data():
    print("Creating sample data...")
    
    # Create membership plans
    basic_plan, _ = MembershipPlan.objects.get_or_create(
        name='basic',
        defaults={
            'display_name': 'Basic Plan',
            'price': 29.99,
            'duration_months': 1,
            'class_booking_limit': 2,
            'description': 'Access to basic gym facilities and 2 classes per week',
            'features': ['Gym access', '2 classes/week', 'Basic exercises']
        }
    )
    
    premium_plan, _ = MembershipPlan.objects.get_or_create(
        name='premium',
        defaults={
            'display_name': 'Premium Plan',
            'price': 49.99,
            'duration_months': 1,
            'class_booking_limit': 5,
            'description': 'Access to all facilities and 5 classes per week',
            'features': ['Full gym access', '5 classes/week', 'Custom workouts', 'Nutrition tips']
        }
    )
    
    vip_plan, _ = MembershipPlan.objects.get_or_create(
        name='vip',
        defaults={
            'display_name': 'VIP Plan',
            'price': 79.99,
            'duration_months': 1,
            'class_booking_limit': 0,  # unlimited
            'description': 'Unlimited access to everything',
            'features': ['Unlimited everything', 'Personal trainer', 'Advanced analytics', 'Priority booking']
        }
    )
    
    # Create some exercises
    exercises_data = [
        {
            'name': 'Push-ups',
            'description': 'Classic upper body exercise',
            'muscle_groups': 'chest, shoulders, triceps',
            'difficulty_level': 'beginner',
            'required_membership_tier': 'basic',
            'instructions': 'Start in plank position, lower chest to ground, push back up',
            'duration_minutes': 5,
            'calories_burned_per_minute': 8
        },
        {
            'name': 'Squats',
            'description': 'Lower body strength exercise',
            'muscle_groups': 'quadriceps, glutes, hamstrings',
            'difficulty_level': 'beginner',
            'required_membership_tier': 'basic',
            'instructions': 'Stand with feet shoulder-width apart, lower hips back and down',
            'duration_minutes': 5,
            'calories_burned_per_minute': 10
        },
        {
            'name': 'Deadlifts',
            'description': 'Full body compound exercise',
            'muscle_groups': 'hamstrings, glutes, back, traps',
            'difficulty_level': 'intermediate',
            'required_membership_tier': 'premium',
            'instructions': 'Lift weight from ground to hip level, keep back straight',
            'duration_minutes': 10,
            'calories_burned_per_minute': 12
        },
        {
            'name': 'Muscle-ups',
            'description': 'Advanced upper body exercise',
            'muscle_groups': 'lats, chest, shoulders, triceps',
            'difficulty_level': 'advanced',
            'required_membership_tier': 'vip',
            'instructions': 'Pull-up transitioning to dip in one fluid motion',
            'duration_minutes': 15,
            'calories_burned_per_minute': 15
        }
    ]
    
    for exercise_data in exercises_data:
        Exercise.objects.get_or_create(
            name=exercise_data['name'],
            defaults=exercise_data
        )
    
    # Create a trainer user if doesn't exist
    trainer, created = User.objects.get_or_create(
        username='trainer1',
        defaults={
            'email': 'trainer@fitness.com',
            'first_name': 'John',
            'last_name': 'Trainer',
            'is_staff': True
        }
    )
    if created:
        trainer.set_password('trainer123')
        trainer.save()
    
    # Create some fitness classes
    base_time = timezone.now() + timedelta(days=1)
    
    classes_data = [
        {
            'name': 'Morning Yoga',
            'description': 'Relaxing yoga session to start your day',
            'datetime': base_time.replace(hour=8, minute=0),
            'duration_minutes': 60,
            'capacity': 15,
            'required_membership_tier': 'basic',
            'price': 0.00
        },
        {
            'name': 'HIIT Training',
            'description': 'High intensity interval training',
            'datetime': base_time.replace(hour=18, minute=0),
            'duration_minutes': 45,
            'capacity': 12,
            'required_membership_tier': 'premium',
            'price': 0.00
        },
        {
            'name': 'Personal Training',
            'description': 'One-on-one training session',
            'datetime': base_time.replace(hour=10, minute=0),
            'duration_minutes': 60,
            'capacity': 1,
            'required_membership_tier': 'vip',
            'price': 0.00
        }
    ]
    
    for class_data in classes_data:
        FitnessClass.objects.get_or_create(
            name=class_data['name'],
            instructor=trainer,
            defaults=class_data
        )
    
    print("Sample data created successfully!")
    print(f"Created {MembershipPlan.objects.count()} membership plans")
    print(f"Created {Exercise.objects.count()} exercises")
    print(f"Created {FitnessClass.objects.count()} fitness classes")

if __name__ == '__main__':
    create_sample_data()