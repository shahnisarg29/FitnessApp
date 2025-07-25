from django.urls import path
from . import views

urlpatterns = [
    path('', views.FitnessClassListView.as_view(), name='class-list'),
    path('my-bookings/', views.UserClassBookingsView.as_view(), name='user-bookings'),
    path('book/<int:class_id>/', views.book_class, name='book-class'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel-booking'),
]