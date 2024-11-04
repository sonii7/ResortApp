from django.contrib import admin
from django.urls import path
from pages import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='user_login'),  # Updated login view

    path('signup/', views.signup, name='signup'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-reservations/', views.manage_reservations, name='manage_reservations'),
    path('guest-dashboard/', views.guest_dashboard, name='guest_dashboard'),
    path('reservation/', views.reservation_form, name='reservation_form'),
    path('room-management/', views.room_management, name='room_management'),
    path('add-room/', views.add_room, name='add_room'),
    path('update-room/<int:room_id>/', views.update_room, name='update_room'),
    path('delete-room/<int:room_id>/', views.delete_room, name='delete_room'),
    path('available-rooms/', views.available_rooms, name='available_rooms'),
   path('book-room/<int:room_id>/', views.book_room, name='book_room'),  # Add this line
    path('payments/', views.payment_page, name='payment_page'),
    path('housekeeping/', views.housekeeping, name='housekeeping'),
    path('housekeeping/filter/', views.filter_rooms, name='filter_rooms'),
    path('contact/', views.contact, name='contact'),
    path('faqs/', views.faqs, name='faqs'),
    path('edit-reservation/<int:reservation_id>/', views.edit_reservation, name='edit_reservation'),
    path('update-reservation/<int:reservation_id>/', views.update_reservation, name='update_reservation'),
    path('cancel-reservation/<int:reservation_id>/', views.cancel_reservation, name='cancel_reservation'),
    
    path('logout/', views.custom_logout_view, name='logout'),
    path('edit_profile/', views.edit_profile, name='edit_profile'),
    path('logout/', views.custom_logout_view, name='logout'),  # For logging out
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)