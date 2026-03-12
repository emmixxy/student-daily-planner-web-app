from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserPreference, Activity


class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['day_of_week', 'start_time', 'end_time']


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name']
