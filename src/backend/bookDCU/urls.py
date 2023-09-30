from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('login/', views.login, name="login"),
    path('basket/', views.show_basket, name="show_basket"),
    path('previous/', views.previous_bookings, name="previous_bookings"),
    path('upcoming/', views.upcoming_bookings, name="upcoming_bookings"),
    path('addbasket/', views.add_to_basket, name="add_basket"),
    path('addbasket/<str:roomid>/<int:seatnumber>/<str:date>/<str:start_time>/<str:end_time>', views.add_to_basket, name="add_basket"),
    path('removeitem/<int:sbi>', views.remove_item, name="remove_basket"),
    path('bookingform/', views.booking, name="bookingform"), 
    path('cancel-booking/<int:bookingid>', views.cancel_booking, name="cancel_booking"),
    path('resend-booking/<int:bookingid>', views.send_email, name="resend_booking"),
    path('test-seat', views.test_selection, name="test_seat"),
    path('occupied/', views.occupiedSeats, name="occupied_seat"),
    path('booking_details/<int:bookingid>', views.display_booking_details, name="booking_details"),
    path('showseats', views.dynamic_seat_selection, name="dynamic_seat_selection"),
    path('verify_booking/<int:bookingid>', views.verify_booking, name="verify_booking"),
    path('help', views.help, name="help"),
]
