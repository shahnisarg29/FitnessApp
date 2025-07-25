from rest_framework import serializers
from .models import MembershipPlan, UserMembership

class MembershipPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembershipPlan
        fields = '__all__'

class UserMembershipSerializer(serializers.ModelSerializer):
    plan_details = MembershipPlanSerializer(source='plan', read_only=True)
    
    class Meta:
        model = UserMembership
        fields = ['id', 'plan', 'plan_details', 'start_date', 'end_date', 
                 'status', 'auto_renew', 'created_at']
        read_only_fields = ['created_at']