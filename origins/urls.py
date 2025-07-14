from django.urls import path
from .views import OriginListView

urlpatterns = [
    path('', OriginListView.as_view(), name='origin-list'),
] 