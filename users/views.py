from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .forms import ProfileCompletionForm
from .serializers import UserSerializer

@login_required
def complete_profile(request):
    """
    Display and process the profile completion form.
    """
    if request.method == "POST":
        form = ProfileCompletionForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/')  # Redirect to home or dashboard
    else:
        form = ProfileCompletionForm(instance=request.user)
    return render(request, 'users/complete_profile.html', {'form': form})


class MeView(APIView):
    """
    API-based version of the current logged-in user's profile.
    Used by the frontend dashboard to show XP, Level, Avatar, etc.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
