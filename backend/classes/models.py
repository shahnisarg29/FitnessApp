from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class FitnessClass(models.Model):
    MEMBERSHIP_TIER_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('vip', 'VIP'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='teaching_classes')
    datetime = models.DateTimeField()
    duration_minutes = models.IntegerField(default=60)
    capacity = models.IntegerField(default=20)
    required_membership_tier = models.CharField(max_length=20, choices=MEMBERSHIP_TIER_CHOICES, default='basic')
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.datetime.strftime('%Y-%m-%d %H:%M')}"

    @property
    def available_spots(self):
        booked_count = self.bookings.filter(status='booked').count()
        return self.capacity - booked_count

    @property
    def is_full(self):
        return self.available_spots <= 0

    class Meta:
        db_table = 'fitness_classes'
        ordering = ['datetime']

class ClassBooking(models.Model):
    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
        ('attended', 'Attended'),
        ('no_show', 'No Show'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='class_bookings')
    fitness_class = models.ForeignKey(FitnessClass, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    notes = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.fitness_class.name} - {self.status}"

    def clean(self):
        # Check if class is full
        if self.fitness_class.is_full and self.status == 'booked':
            raise ValidationError("This class is full.")

    class Meta:
        db_table = 'class_bookings'
        unique_together = ['user', 'fitness_class']  # User can't book same class twice