from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from .models import FitnessClass, ClassBooking
from .serializers import FitnessClassSerializer, ClassBookingSerializer

class FitnessClassListView(generics.ListAPIView):
    serializer_class = FitnessClassSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return FitnessClass.objects.filter(
            datetime__gte=timezone.now(),
            is_active=True
        ).order_by('datetime')

class UserClassBookingsView(generics.ListAPIView):
    serializer_class = ClassBookingSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return ClassBooking.objects.filter(user=self.request.user).order_by('-booking_date')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def book_class(request, class_id):
    try:
        fitness_class = FitnessClass.objects.get(id=class_id)
        
        # Check if class is full
        if fitness_class.is_full:
            return Response({'error': 'Class is full'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if user already booked this class
        if ClassBooking.objects.filter(user=request.user, fitness_class=fitness_class).exists():
            return Response({'error': 'Already booked this class'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create booking
        booking = ClassBooking.objects.create(
            user=request.user,
            fitness_class=fitness_class,
            status='booked'
        )
        
        return Response({
            'message': 'Class booked successfully!',
            'booking': ClassBookingSerializer(booking).data
        }, status=status.HTTP_201_CREATED)
        
    except FitnessClass.DoesNotExist:
        return Response({'error': 'Class not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def cancel_booking(request, booking_id):
    try:
        booking = ClassBooking.objects.get(id=booking_id, user=request.user)
        booking.status = 'cancelled'
        booking.save()
        return Response({'message': 'Booking cancelled successfully'})
    except ClassBooking.DoesNotExist:
        return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)