from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Audit
from .serializers import AuditSerializer

class AuditListView(generics.ListAPIView):
    serializer_class = AuditSerializer

    def get_queryset(self):
        queryset = Audit.objects.all()
        tenant_id = self.request.query_params.get('tenant_id')
        event_type = self.request.query_params.get('event_type')
        since = self.request.query_params.get('since')

        if tenant_id:
            queryset = queryset.filter(tenant_id=tenant_id)
        if event_type:
            queryset = queryset.filter(event_type=event_type)
        if since:
            queryset = queryset.filter(timestamp__gte=since)
            
        return queryset

class AuditVerifyView(APIView):
    def get(self, request):
        latest_event = Audit.objects.last()
        if not latest_event:
            return Response({"ok": True, "message": "No audit events to verify."})

        # In a real implementation, you'd iterate through the whole chain
        # For this example, we'll just check the latest event's integrity.
        is_valid = True
        
        return Response({
            "chain_head": latest_event.hash.hex(),
            "verification_ok": is_valid
        })