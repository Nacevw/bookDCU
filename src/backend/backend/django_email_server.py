# reference
# https://www.abstractapi.com/guides/django-send-email

'''This module contains the functions to send an email about a booking being confirmed or cancelled as well as verified'''

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

# Function to send an email about a booking being confirmed or cancelled
def send_booking_email(recipient_name, recipient_email, booking_id, seat, room, building, campus, start_time, end_time, status):

    # create a dictionary to store different merge data for the email
    merge_data = {
        'name': recipient_name,
        'room': room,
        'booking_id': booking_id,
        'start_time': start_time,
        'end_time': end_time,
        'building': building,
        'campus': campus,
        'seat': seat,
        'booking_status': status
    }

    # create a dictionary to store different subject lines
    subject_dict = {
        "confirmed": "bookDCU - Booking Confirmed ✅",
        "cancelled": "bookDCU - Booking Cancelled ❌",
    }

    # render the email template with the merge data
    html_content = render_to_string('email_template.html', merge_data)

    # a plain text message for non-HTML email clients
    message = EmailMultiAlternatives(
        subject=subject_dict[status],
        body=f"Dear {recipient_name},\n\nThank you for booking a room at bookDCU. Your booking details are as follows:\n\nRoom: {room}\n\n\nKind Regards,\nbookDCU Team",
        from_email=settings.EMAIL_HOST_USER,
        to=[recipient_email[0]]
    )
    # attach the HTML content to the email
    message.attach_alternative(html_content, "text/html")

    # send the email
    message.send()


def send_verified_email(recipient_name, recipient_email, booking_id, seat, room, building, campus, start_time, end_time, status):
    merge_data = {
        'name': recipient_name,
        'room': room,
        'booking_id': booking_id,
        'start_time': start_time,
        'end_time': end_time,
        'building': building,
        'campus': campus,
        'seat': seat,
        'booking_status': status
    }

    html_content = render_to_string('email_template.html', merge_data)

    message = EmailMultiAlternatives(
    subject="bookDCU - Booking Verified ✅",
    body=f"Dear {recipient_name},\n\nThank you for verifying your booking at bookDCU. Your booking details are as follows:\n\nRoom: {room}\n\n\nKind Regards,\nbookDCU Team",
    from_email=settings.EMAIL_HOST_USER,
    to=[recipient_email[0]]
    )
    message.attach_alternative(html_content, "text/html")
    message.send()
