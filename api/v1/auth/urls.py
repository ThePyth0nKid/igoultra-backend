from django.urls import path, include

urlpatterns = [
    # DJ Rest Auth endpoints for session login/logout
    path('', include('dj_rest_auth.urls')),
    # Registration endpoints (including social login)
    path('registration/', include('dj_rest_auth.registration.urls')),
]
