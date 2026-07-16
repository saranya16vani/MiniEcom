from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False)  # ✅ add email field from User

    class Meta:
        model = UserProfile
        fields = ["phone_number", "address", "email"]

    def save(self, commit=True):
        profile = super().save(commit=False)
        # Save email to the related User model
        profile.user.email = self.cleaned_data["email"]
        if commit:
            profile.user.save()
            profile.save()
        return profile
