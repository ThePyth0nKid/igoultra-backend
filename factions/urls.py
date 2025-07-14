from django.urls import path
from .views import FactionListView

urlpatterns = [
    path('', FactionListView.as_view(), name='faction-list'),
] 