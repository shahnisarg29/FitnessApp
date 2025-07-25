import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fitness_project.settings')
django.setup()

from django.contrib.auth import get_user_model
from workouts.models import Exercise, Workout, WorkoutExercise

User = get_user_model()

def create_sample_workouts():
    print("Creating sample workouts...")
    
    # Get the exercises we created
    try:
        pushups = Exercise.objects.get(name='Push-ups')
        squats = Exercise.objects.get(name='Squats')
        deadlifts = Exercise.objects.get(name='Deadlifts')
        muscle_ups = Exercise.objects.get(name='Muscle-ups')
    except Exercise.DoesNotExist:
        print("Error: Exercises not found. Please run create_sample_data.py first")
        return
    
    # Get the trainer user
    try:
        trainer = User.objects.get(username='trainer1')
    except User.DoesNotExist:
        print("Error: Trainer user not found. Please run create_sample_data.py first")
        return
    
    # Create beginner workout
    beginner_workout, created = Workout.objects.get_or_create(
        name='Beginner Full Body',
        defaults={
            'description': 'A simple full body workout for beginners',
            'created_by': trainer,
            'required_membership_tier': 'basic',
            'estimated_duration': 30,
            'difficulty_level': 'beginner',
            'is_public': True
        }
    )
    
    if created:
        print("Created Beginner Full Body workout")
        # Add exercises to the workout
        WorkoutExercise.objects.create(
            workout=beginner_workout,
            exercise=pushups,
            sets=3,
            reps=10,
            rest_seconds=60,
            order=1
        )
        WorkoutExercise.objects.create(
            workout=beginner_workout,
            exercise=squats,
            sets=3,
            reps=15,
            rest_seconds=60,
            order=2
        )
    else:
        print("Beginner Full Body workout already exists")
    
    # Create intermediate workout
    intermediate_workout, created = Workout.objects.get_or_create(
        name='Strength Builder',
        defaults={
            'description': 'Intermediate workout focusing on strength',
            'created_by': trainer,
            'required_membership_tier': 'premium',
            'estimated_duration': 45,
            'difficulty_level': 'intermediate',
            'is_public': True
        }
    )
    
    if created:
        print("Created Strength Builder workout")
        WorkoutExercise.objects.create(
            workout=intermediate_workout,
            exercise=pushups,
            sets=4,
            reps=15,
            rest_seconds=90,
            order=1
        )
        WorkoutExercise.objects.create(
            workout=intermediate_workout,
            exercise=squats,
            sets=4,
            reps=20,
            rest_seconds=90,
            order=2
        )
        WorkoutExercise.objects.create(
            workout=intermediate_workout,
            exercise=deadlifts,
            sets=3,
            reps=8,
            rest_seconds=120,
            order=3
        )
    else:
        print("Strength Builder workout already exists")
    
    # Create advanced workout
    advanced_workout, created = Workout.objects.get_or_create(
        name='Elite Training',
        defaults={
            'description': 'Advanced workout for experienced athletes',
            'created_by': trainer,
            'required_membership_tier': 'vip',
            'estimated_duration': 60,
            'difficulty_level': 'advanced',
            'is_public': True
        }
    )
    
    if created:
        print("Created Elite Training workout")
        WorkoutExercise.objects.create(
            workout=advanced_workout,
            exercise=muscle_ups,
            sets=5,
            reps=5,
            rest_seconds=180,
            order=1
        )
        WorkoutExercise.objects.create(
            workout=advanced_workout,
            exercise=deadlifts,
            sets=5,
            reps=5,
            rest_seconds=180,
            order=2
        )
    else:
        print("Elite Training workout already exists")
    
    print(f"Total workouts in database: {Workout.objects.count()}")

if __name__ == '__main__':
    create_sample_workouts()