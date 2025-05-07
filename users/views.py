from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import ProfileCompletionForm

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