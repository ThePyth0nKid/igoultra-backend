from django.urls import path, include

urlpatterns = [
    path("auth/", include("api.v1.auth.urls")),
    path("user/", include("api.v1.user.urls")),
    path("xp/", include("api.v1.xp.urls")),
    path("seasons/", include("api.v1.seasons.urls")),
    path("rankings/", include("api.v1.rankings.urls")),
]
