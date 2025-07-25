from django.urls import path
from . import views

urlpatterns = [
    path('plans/', views.MembershipPlanListView.as_view(), name='membership-plans'),
    path('my-membership/', views.user_membership, name='user-membership'),
    path('purchase/<int:plan_id>/', views.purchase_membership, name='purchase-membership'),
]