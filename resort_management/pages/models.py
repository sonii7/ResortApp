from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    

    def __str__(self):
        return f"{self.user.username}'s Profile"

class Room(models.Model):
    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=[('Available', 'Available'), ('Occupied', 'Occupied')])

    def __str__(self):
        return f'Room {self.room_number} ({self.room_type})'

class Reservation(models.Model):
    ROOM_TYPES = [
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('suite', 'Suite'),
    ]

    DINNER_TYPES = [
        ('couple', 'General'),
        ('family', 'Family/Friends'),
        ('businessmeet', 'Business Meet'),
    ]

    guest_name = models.CharField(max_length=100)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    room_type = models.CharField(max_length=50, choices=ROOM_TYPES)  # Added choices for room type
    dinner_preference = models.CharField(max_length=50) # Added dinner type field
    status = models.CharField(max_length=50, default="Pending")  # Default status

    def __str__(self):
        return f"Reservation {self.id} - {self.guest_name}"

class Housekeeping(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    date = models.DateField()
    is_cleaned = models.BooleanField(default=False)

    def __str__(self):
        return f"Housekeeping for Room {self.room.room_number} on {self.date}"

