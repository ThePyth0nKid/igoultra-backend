from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from xp.models import XpType, XpEvent
from xp.services import add_xp_to_user, get_xp_stats, xp_for_level
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
    Antwort enthält jetzt auch Level- und Next-Level-Infos.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = AddXpSerializer

    def post(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        # XP hinzufügen
        result = add_xp_to_user(
            user=request.user,
            type_key=ser.validated_data['key'],
            amount_units=ser.validated_data['amount_units'],
            metadata=ser.validated_data.get('metadata')
        )

        # Level-Statistiken ermitteln
        stats = get_xp_stats(request.user)

        # Kombinierte Antwort
        response_data = {
            'awarded_xp':        result['awarded_xp'],
            'total_xp':          stats['total_xp'],
            'level':             stats['level'],
            'next_level':        stats['next_level'],
            'next_level_xp':     stats['next_level_xp'],
            'xp_to_next':        stats['xp_to_next'],
            'leveled_up':        result['leveled_up'],
        }
        return Response(response_data, status=status.HTTP_200_OK)


class XpStatsView(generics.GenericAPIView):
    """
    GET /api/v1/xp/stats/ → Aktuelle XP- und Level-Statistiken
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        stats = get_xp_stats(request.user)
        return Response(stats, status=status.HTTP_200_OK)


class XpHistoryView(generics.ListAPIView):
    """
    GET /api/v1/xp/history/ → Historie der XpEvents des aktuellen Users
    Antwort erweitert um das Level zum Zeitpunkt jedes Events.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = XpEventSerializer

    def get_queryset(self):
        # Wir holen alle Events, und annotieren das Level *nach* jedem Event.
        events = XpEvent.objects.filter(user=self.request.user).order_by('timestamp')
        # Da wir das per SQL nicht leicht machen können, würden wir hier
        # im Serializer das Level pro Event berechnen, oder
        # wir fügen es als extra-Feld hinzu:
        # Zum MVP belassen wir es im Serializer.
        return events
