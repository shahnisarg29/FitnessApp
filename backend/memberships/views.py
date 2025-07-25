from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.utils import timezone
from datetime import timedelta
from .models import MembershipPlan, UserMembership
from .serializers import MembershipPlanSerializer, UserMembershipSerializer

class MembershipPlanListView(generics.ListAPIView):
    queryset = MembershipPlan.objects.filter(is_active=True)
    serializer_class = MembershipPlanSerializer
    permission_classes = [IsAuthenticated]

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_membership(request):
    try:
        membership = UserMembership.objects.get(user=request.user)
        serializer = UserMembershipSerializer(membership)
        return Response(serializer.data)
    except UserMembership.DoesNotExist:
        return Response({'message': 'No active membership found'}, status=404)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def purchase_membership(request, plan_id):
    try:
        plan = MembershipPlan.objects.get(id=plan_id)
        
        # Check if user already has an active membership
        existing_membership = UserMembership.objects.filter(
            user=request.user, 
            status='active'
        ).first()
        
        if existing_membership:
            # Update existing membership
            existing_membership.plan = plan
            existing_membership.start_date = timezone.now()
            existing_membership.end_date = timezone.now() + timedelta(days=30 * plan.duration_months)
            existing_membership.save()
            membership = existing_membership
        else:
            # Create new membership
            membership = UserMembership.objects.create(
                user=request.user,
                plan=plan,
                start_date=timezone.now(),
                end_date=timezone.now() + timedelta(days=30 * plan.duration_months),
                status='active'
            )
        
        return Response({
            'message': 'Membership purchased successfully!',
            'membership': UserMembershipSerializer(membership).data
        })
        
    except MembershipPlan.DoesNotExist:
        return Response({'error': 'Membership plan not found'}, status=404)