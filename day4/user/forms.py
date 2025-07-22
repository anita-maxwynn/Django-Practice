from django import forms
from .models import Profile, Result

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100, required=True)
    roll = forms.IntegerField(required=True)
    email = forms.EmailField(required=True)
    city = forms.CharField(max_length=100, required=True)

    def save(self):
        profile = Profile(
            name=self.cleaned_data['name'],
            roll=self.cleaned_data['roll'],
            email=self.cleaned_data['email'],
            city=self.cleaned_data['city']
        )
        profile.save()
        return profile