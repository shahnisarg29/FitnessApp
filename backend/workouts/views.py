from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Exercise, Workout, WorkoutLog
from .serializers import ExerciseSerializer, WorkoutSerializer, WorkoutLogSerializer

class ExerciseListView(generics.ListAPIView):
    queryset = Exercise.objects.all()  # Show all for now
    serializer_class = ExerciseSerializer
    permission_classes = []  # Remove authentication

class WorkoutListView(generics.ListAPIView):
    queryset = Workout.objects.filter(is_public=True)  # Show all public workouts
    serializer_class = WorkoutSerializer
    permission_classes = []  # Remove authentication

class WorkoutLogListCreateView(generics.ListCreateAPIView):
    queryset = WorkoutLog.objects.all()
    serializer_class = WorkoutLogSerializer
    permission_classes = [IsAuthenticated]  # Require authentication

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)