from django.urls import path
from .views import XpTypeListView, AddXpView, XpHistoryView

urlpatterns = [
    path('types/',   XpTypeListView.as_view(),  name='xp-types'),
    path('add/',     AddXpView.as_view(),       name='xp-add'),
    path('history/', XpHistoryView.as_view(),   name='xp-history'),
]
