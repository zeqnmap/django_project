from django import forms
from .models import Profile

class ProfileAvatarForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = "avatar", "bio"
        widgets = {
            'avatar': forms.FileInput(attrs={'accept': 'image/*'})
        }