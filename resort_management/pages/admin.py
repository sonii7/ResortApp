from django.contrib import admin

# Register your models here.
# pages/admin.py
from django.contrib import admin
from .models import Room, Reservation, Housekeeping

admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Housekeeping)
