from django.shortcuts import redirect
from django.urls import reverse

class EnsureProfileComplete:
    """
    Redirects authenticated users without an ultra_name
    to the profile completion page.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = request.user
        # only enforce for logged-in non-staff users
        if user.is_authenticated and not user.is_staff:
            # skip the completion URL itself to avoid loops
            if not user.ultra_name and not request.path.startswith(reverse("complete_profile")):
                return redirect("complete_profile")
        return self.get_response(request)
