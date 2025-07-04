from django.urls import path
from .views import LayerListView, MyUserLayerProgressView

urlpatterns = [
    path('', LayerListView.as_view(), name='layer-list'),
    path('progress/me/', MyUserLayerProgressView.as_view(), name='my-user-layer-progress'),
] 