from django import forms
from .models import User

class ProfileCompletionForm(forms.ModelForm):
    """
    Form for completing user profile after Discord login.
    """
    class Meta:
        model = User
        fields = ["ultra_name", "email", "avatar_url"]