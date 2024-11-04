from django.shortcuts import render, get_object_or_404, redirect
from .models import Room, Reservation
from .forms import SignupForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib import messages  # Added for showing success/error messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import EditProfileForm
from django.utils.dateparse import parse_date
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import update_session_auth_hash
from pages.models import UserProfile

# Renamed your login view to avoid the conflict with Django's built-in 'login' function
def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)  # Use the aliased login function 'auth_login'
            if user.is_superuser:
                return redirect('pages:admin_dashboard')
            else:
                return redirect('pages:guest_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    
    return render(request, 'login.html')


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])  # Set the password
            user.save()  # Save the user
            messages.success(request, "Account created successfully. Please log in.")
            return redirect('pages:user_login')  # Redirect to login page after successful signup
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


@login_required
def admin_dashboard(request):
    # This view will be accessible only to superusers
    if request.user.is_superuser:
        return render(request, 'admin_dashboard.html')
    else:
        return HttpResponse("You are not authorized to access this page.")

@login_required
def guest_dashboard(request):
    # Ensure the user is logged in, otherwise redirect to login page
    return render(request, 'guest_dashboard.html')



def reservation_form(request):
    if request.method == 'POST':
        guest_name = request.POST.get('name')
        checkin_date = request.POST.get('checkin')
        checkout_date = request.POST.get('checkout')
        room_type = request.POST.get('room')  
        dinner_preference = request.POST.get('members')  

       
        if not (guest_name and checkin_date and checkout_date and room_type):
            return render(request, 'reservation_form.html', {
                'error_message': 'Please fill all the required fields.'
            })

        # Reservation object
        new_reservation = Reservation(
            guest_name=guest_name,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            room_type=room_type,  
            dinner_preference=dinner_preference,  
            status='Confirmed'  
        )
        new_reservation.save()  
        return redirect('pages:available_rooms')  

    return render(request, 'reservation_form.html')


def room_management(request):
    rooms = Room.objects.all()
    return render(request, 'room_management.html', {'rooms': rooms})


def add_room(request):
    if request.method == 'POST':
        room_number = request.POST['room_number']
        room_type = request.POST['room_type']
        status = request.POST['status']
        Room.objects.create(room_number=room_number, room_type=room_type, status=status)
        return redirect('pages:room_management')


def update_room(request, room_id):
    if request.method == 'POST':
        room = Room.objects.get(id=room_id)
        room.room_number = request.POST['room_number']
        room.room_type = request.POST['room_type']
        room.status = request.POST['status']
        room.save()
        return redirect('pages:room_management')


def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    room.delete()
    return redirect('pages:room_management')


def payment_page(request):
    return render(request, 'payment_page.html')


def housekeeping(request):
    return render(request, 'housekeeping.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        # Construct the email
        subject = f"New contact form submission from {name}"
        email_message = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage:\n{message}"
        recipient_list = ['sonika.n1137@gmail.com']  # Replace with the recipient email

        try:
            send_mail(subject, email_message, settings.DEFAULT_FROM_EMAIL, recipient_list)
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')  # Redirect to the contact page or any page you want
        except Exception as e:
            messages.error(request, f'An error occurred: {e}')

    return render(request, 'contact.html') 


def manage_reservations(request):
    reservations = Reservation.objects.all()
    
    if request.method == 'POST':
        # Get reservation id and other form data
        reservation_id = request.POST.get('reservation_id')
        reservation = get_object_or_404(Reservation, pk=reservation_id)

        # Retrieve and validate form data
        guest_name = request.POST.get('guest_name')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        room_type = request.POST.get('room_type')
        status = request.POST.get('status')

        # Validation: ensure all fields are present
        if not all([guest_name, checkin_date, checkout_date, room_type, status]):
            messages.error(request, "All fields are required.")
            return render(request, 'manage_reservations.html', {'reservations': reservations})

        # Parse dates
        checkin_date = parse_date(checkin_date)
        checkout_date = parse_date(checkout_date)

        if not checkin_date or not checkout_date:
            messages.error(request, "Invalid date format.")
            return render(request, 'manage_reservations.html', {'reservations': reservations})

        # Update reservation
        reservation.guest_name = guest_name
        reservation.checkin_date = checkin_date
        reservation.checkout_date = checkout_date
        reservation.room_type = room_type
        reservation.status = status
        reservation.save()

        # Confirmation message
        messages.success(request, "Reservation updated successfully!")
        return redirect('pages:manage_reservations')  # Redirect to avoid re-posting on page reload

    # Display the manage reservations page with the form embedded
    return render(request, 'manage_reservations.html', {'reservations': reservations})

def faqs(request):
    return render(request, 'faqs.html')

def edit_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    
    if request.method == 'POST':
        # Retrieve form data
        guest_name = request.POST.get('guest_name')
        checkin_date = request.POST.get('checkin_date')
        checkout_date = request.POST.get('checkout_date')
        room_type = request.POST.get('room_type')
        status = request.POST.get('status')

        # Basic validation
        if not all([guest_name, checkin_date, checkout_date, room_type, status]):
            messages.error(request, "All fields are required.")
            return render(request, 'edit_reservation.html', {'reservation': reservation})

        # Parse dates to ensure they are valid
        checkin_date = parse_date(checkin_date)
        checkout_date = parse_date(checkout_date)

        if not checkin_date or not checkout_date:
            messages.error(request, "Invalid date format.")
            return render(request, 'edit_reservation.html', {'reservation': reservation})
        
        # Update reservation
        reservation.guest_name = guest_name
        reservation.checkin_date = checkin_date
        reservation.checkout_date = checkout_date
        reservation.room_type = room_type
        reservation.status = status
        reservation.save()

        # Redirect on success
        return redirect('pages:manage_reservations')
    
    # Render the edit reservation page
    return render(request, 'edit_reservation.html', {'reservation': reservation})

def update_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == 'POST':
        # Update fields based on POST data
        reservation.room_type = request.POST.get('room_type')
        reservation.status = request.POST.get('status')
        reservation.save()
        return redirect('pages:manage_reservations')
    return render(request, 'update_reservation.html', {'reservation': reservation})


def cancel_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation, pk=reservation_id)
    if request.method == 'POST':
        reservation.delete()
        return redirect('pages:manage_reservations')
    return render(request, 'cancel_reservation.html', {'reservation': reservation})

def filter_rooms(request):
    status = request.GET.get('status')
    if status:
        rooms = Room.objects.filter(status=status)
    else:
        rooms = Room.objects.all()  # Fetch all rooms if no filter is selected
    return render(request, 'housekeeping.html', {'rooms': rooms})

# pages/views.py

def available_rooms(request):
    rooms = Room.objects.filter(status='Available')
    return render(request, 'available_rooms.html', {'rooms': rooms})


def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)

    if request.method == 'POST':
        guest_name = request.POST.get('name')
        checkin_date = request.POST.get('checkin')
        checkout_date = request.POST.get('checkout')
        room_type = room.room_type
        dinner_preference = request.POST.get('members')  # Ensure this field is correct

        if not (guest_name and checkin_date and checkout_date):
            return render(request, 'payment_page.html', {
                'room': room,
                'error_message': 'Please fill all the required fields.'
            })

        # Save the reservation to the database
        Reservation.objects.create(
            guest_name=guest_name,
            checkin_date=checkin_date,
            checkout_date=checkout_date,
            room_type=room_type,
            dinner_preference=dinner_preference
        )
        
        # Add a success message
        messages.success(request, 'Your booking has been successfully made!')

        return redirect('pages:manage_reservations')  # Redirect to the reservations management page

    return render(request, 'available_rooms.html', {'room': room})

@login_required
def edit_profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Handle profile update
        form = EditProfileForm(request.POST, request.FILES, instance=user_profile, user=request.user)
        if form.is_valid():
            # Save profile information
            form.save()
            messages.success(request, 'Profile updated successfully!')

            # Handle password change
            password = request.POST.get('password')
            password_confirm = request.POST.get('password_confirm')
            if password and password == password_confirm:
                user = request.user
                user.set_password(password)
                user.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(request, 'Password updated successfully!')
            else:
                messages.error(request, 'Password mismatch. Please try again.')
            
            return redirect('pages:edit_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = EditProfileForm(instance=user_profile, user=request.user)

    return render(request, 'edit_profile.html', {'form': form})

# Custom logout view
def custom_logout_view(request):
    logout(request)
    return redirect('login')

def custom_logout_view(request):
    logout(request)
    return redirect('login')

