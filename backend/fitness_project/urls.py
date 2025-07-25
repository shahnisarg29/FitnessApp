from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/login/', obtain_auth_token, name='api-login'),
    path('api/users/', include('users.urls')),
    path('api/memberships/', include('memberships.urls')),
    path('api/workouts/', include('workouts.urls')),
    path('api/classes/', include('classes.urls')),
]