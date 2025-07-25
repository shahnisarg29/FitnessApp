from rest_framework import serializers
from .models import Exercise, Workout, WorkoutExercise, WorkoutLog

class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class WorkoutExerciseSerializer(serializers.ModelSerializer):
    exercise_details = ExerciseSerializer(source='exercise', read_only=True)
    
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'exercise_details', 'sets', 'reps', 
                 'duration_seconds', 'rest_seconds', 'order']

class WorkoutSerializer(serializers.ModelSerializer):
    exercises_detail = WorkoutExerciseSerializer(source='workoutexercise_set', 
                                                many=True, read_only=True)
    created_by_name = serializers.CharField(source='created_by.username', read_only=True)
    
    class Meta:
        model = Workout
        fields = ['id', 'name', 'description', 'created_by', 'created_by_name',
                 'required_membership_tier', 'estimated_duration', 'difficulty_level',
                 'is_public', 'created_at', 'exercises_detail']
        read_only_fields = ['created_at']

class WorkoutLogSerializer(serializers.ModelSerializer):
    workout_details = WorkoutSerializer(source='workout', read_only=True)
    
    class Meta:
        model = WorkoutLog
        fields = ['id', 'workout', 'workout_details', 'completed_at', 
                 'duration_minutes', 'notes']
        read_only_fields = ['completed_at']