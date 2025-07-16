from django.urls import path
from .views import MeView, AvatarS3PresignView, AvatarView

urlpatterns = [
    path("me/", MeView.as_view(), name="custom_me_view"),
    path("avatar/presign/", AvatarS3PresignView.as_view(), name="avatar_presign"),
    path("avatar/", AvatarView.as_view(), name="avatar"),
]
