from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Exercise(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    
    MEMBERSHIP_TIER_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    muscle_groups = models.CharField(max_length=200, help_text="Comma-separated muscle groups")
    difficulty_level = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES)
    required_membership_tier = models.CharField(max_length=20, choices=MEMBERSHIP_TIER_CHOICES, default='basic')
    instructions = models.TextField(blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    calories_burned_per_minute = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'exercises'

class Workout(models.Model):
    MEMBERSHIP_TIER_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    exercises = models.ManyToManyField(Exercise, through='WorkoutExercise')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_workouts')
    required_membership_tier = models.CharField(max_length=20, choices=MEMBERSHIP_TIER_CHOICES, default='basic')
    estimated_duration = models.IntegerField(help_text="Duration in minutes")
    difficulty_level = models.CharField(max_length=20, choices=Exercise.DIFFICULTY_CHOICES)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'workouts'

class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    sets = models.IntegerField(default=1)
    reps = models.IntegerField(null=True, blank=True)
    duration_seconds = models.IntegerField(null=True, blank=True)
    rest_seconds = models.IntegerField(default=60)
    order = models.IntegerField(default=0)

    class Meta:
        db_table = 'workout_exercises'
        ordering = ['order']

class WorkoutLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workout_logs')
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE)
    completed_at = models.DateTimeField(auto_now_add=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.workout.name} - {self.completed_at.date()}"

    class Meta:
        db_table = 'workout_logs'