# forms.py in your 'reservations' app

from django import forms
from .models import Reservation
from django.contrib.auth.models import User
from .models import UserProfile

class EditProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput, label="New Password")
    password_confirm = forms.CharField(max_length=128, required=False, widget=forms.PasswordInput, label="Confirm New Password")

    class Meta:
        model = UserProfile
        fields = ['avatar']  # Avatar and phone_number from UserProfile

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        super().__init__(*args, **kwargs)
        self.fields['username'].initial = self.user.username
        self.fields['email'].initial = self.user.email
        

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password != password_confirm:
            self.add_error('password_confirm', "Passwords do not match.")

    def save(self, commit=True):
        user_profile = super().save(commit=False)
        user = self.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']


        # Set the new password if provided
        password = self.cleaned_data.get('password')
        if password:
            user.set_password(password)

        if commit:
            user.save()
            user_profile.save()
        return user_profile
    
class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['guest_name', 'checkin_date', 'checkout_date', 'room_type', 'dinner_preference']
        

    
class SignupForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']