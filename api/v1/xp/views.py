from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from xp.models import XpType, XpEvent
from xp.services import add_xp_to_user
from xp.serializers import XpTypeSerializer, XpEventSerializer, AddXpSerializer

class XpTypeListView(generics.ListAPIView):
    """
    GET /api/v1/xp/types/ → Liste aller konfigurierten XpTypes
    """
    permission_classes = [IsAuthenticated]
    queryset = XpType.objects.all()
    serializer_class = XpTypeSerializer

class AddXpView(generics.GenericAPIView):
    """
    POST /api/v1/xp/add/ → XP für den aktuellen User vergeben
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddXpSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        result = add_xp_to_user(
            user=request.user,
            type_key=ser.validated_data['key'],
            amount_units=ser.validated_data['amount_units'],
            metadata=ser.validated_data.get('metadata')
        )
        return Response(result, status=status.HTTP_200_OK)

class XpHistoryView(generics.ListAPIView):
    """
    GET /api/v1/xp/history/ → Historie der XpEvents des aktuellen Users
    """
    permission_classes = [IsAuthenticated]
    serializer_class = XpEventSerializer

    def get_queryset(self):
        return XpEvent.objects.filter(user=self.request.user)
