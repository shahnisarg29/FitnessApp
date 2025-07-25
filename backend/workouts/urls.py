from django.urls import path
from . import views

urlpatterns = [
    path('exercises/', views.ExerciseListView.as_view(), name='exercise-list'),
    path('workouts/', views.WorkoutListView.as_view(), name='workout-list'),
    path('logs/', views.WorkoutLogListCreateView.as_view(), name='workout-logs'),
]