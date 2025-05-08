from django.urls import path, include
from users.views import MeView

urlpatterns = [
    # DJ Rest Auth endpoints for session login/logout
    path('', include('dj_rest_auth.urls')),
    # Registration endpoints (including social login)
    path('registration/', include('dj_rest_auth.registration.urls')),
    path('me/', MeView.as_view(), name="custom_me_view"),
]
