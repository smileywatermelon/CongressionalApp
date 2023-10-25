from django import forms
from .models import User, Profile, Post


class UserForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ("username", "password")

    def save(self, commit=True):
        data = self.cleaned_data
        user = User(username=data["username"], password=data["password"])
        # makes user profile in profile table in models
        profile = Profile(display_name=user.username, user=user)
        if commit:
            user.save()
            # saves profile to profile table in models
            profile.save()
