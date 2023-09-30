import json
from datetime import date, datetime, time, timedelta

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from backend.django_email_server import *

from .forms import *
from .models import *

# Django views -------------------------------------------------------.
@login_required
def index(request):
    if request.method == 'POST':
        # get the data from the form and navigate to the room selection page
        form = DateTimeForm(request.POST)

        if form.is_valid():
            # get the data from the form
            date = form.cleaned_data['date']

            # convert the date to a datetime object
            # pretty date is the date in a format like Monday, 1st January.
            pretty_date = datetime.strptime(date.strftime('%Y-%m-%d'), '%Y-%m-%d').strftime('%A, %B %d')

            start_time = form.cleaned_data['start_time']
            end_time = form.cleaned_data['end_time']

            # format the date to always be of the form YYYY-abbreviated-month-DD
            date = datetime.strptime(date.strftime('%Y-%m-%d'), '%Y-%m-%d').strftime('%Y-%b-%d')

            # get the rooms that are available for the given time
            rooms = Room.objects.all()
            availableRooms = []
            for room in rooms:
                # check if the room is available
                # if room.is_available(start_time, end_time):
                availableRooms.append(room)
            # return render(request, 'available_rooms.html', {'rooms': availableRooms})
            return render(request, 'test-seat.html', {'date': date, 'start_time': start_time, 'end_time': end_time, 'pretty_date' : pretty_date, 'rooms': availableRooms})
        else:
            return render(request, 'index.html', {'form': form})
    else:
        form = DateTimeForm()
        return render(request, 'index.html', {'form': form})

def login(request):
    return render(request, 'login.html')

@login_required
def basket(request):
    return render(request, 'basket.html')

@login_required
def previous_bookings(request):
    user = request.user

    # create a datetime object for the current date and time
    current_datetime = datetime.combine(date.today(), datetime.now().time())
    pastBookings = []
    bookings = Booking.objects.filter(user_id=user)
    for booking in bookings:
        # create a datetime object for the booking end time
        booking_datetime = datetime.combine(booking.end_time.date(), booking.end_time.time())

        if booking_datetime < current_datetime:
            pastBookings.append(booking)
    return render(request, 'previous_bookings.html', {'bookings': pastBookings})


@login_required
def upcoming_bookings(request):
    user = request.user

    futureBookings = []
    bookings = Booking.objects.filter(user_id=user)
    current_datetime = datetime.combine(date.today(), datetime.now().time())

    for booking in bookings:
        booking_datetime = datetime.combine(booking.end_time.date(), booking.end_time.time())
        # if the booking end time is after the current time
        if booking_datetime > current_datetime:
            futureBookings.append(booking)
    return render(request, 'upcoming_bookings.html', {'bookings': futureBookings})

@login_required
def add_to_basket(request, roomid, seatnumber, date, start_time, end_time):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()

    # convert the date from the format like 2023-Mar-01 to a datetime object
    date = datetime.strptime(date, '%Y-%b-%d').date()

    # convert the start and end times from strings like 17:00:00 to datetime objects
    start_time = datetime.strptime(start_time, '%H:%M:%S').time()
    end_time = datetime.strptime(end_time, '%H:%M:%S').time()

    start_datetime = datetime.combine(date, start_time) 
    end_datetime = datetime.combine(date, end_time)

    if basket is None:
        # no basket exists, create one
        Basket.objects.create(user_id=user)
        basket = Basket.objects.filter(user_id=user, is_active=True).first()
    room = Room.objects.get(id=roomid)
    sbi = BasketItem.objects.filter(basket_id=basket, room_id=room).first()
    if sbi is None:
        # there is no basket item for that booking
        # create one
        sbi = BasketItem(basket_id=basket, room_id=room, user_id=user,
                         name=user.username, seat_number=seatnumber, start_time=start_datetime, end_time=end_datetime)
        sbi.save()
        return redirect('bookingform')
    else:
        # that room is already in the basket
        # return an error
        sbi.delete()
        sbi = BasketItem(basket_id=basket, room_id=room, user_id=user,
                         name=user.username, seat_number=seatnumber, start_time=start_datetime, end_time=end_datetime)
        sbi.save()
        return redirect('bookingform')

@login_required
def show_basket(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()

    if basket is None:
        return render(request, 'basket.html', {'empty': True})
    else:
        sbi = BasketItem.objects.filter(basket_id=basket)
        if sbi.exists():
            return render(request, 'basket.html', {'basket': basket, 'sbi': sbi})
        else:
            return render(request, 'basket.html', {'empty': True})


@login_required
def remove_item(request, sbi):
    basketitem = BasketItem.objects.get(id=sbi)
    if basketitem is None:
        return redirect("/basket")  # if error redirect to shopping basket
    else:
        #  delete the basket item
        basketitem.delete()
    return redirect("/basket")

def cancel_booking(request, bookingid):
    booking = Booking.objects.get(id=bookingid)
    if booking is None:
        return redirect("/upcoming")
    else:
        send_email(request, bookingid, "cancelled")
        seat = Seat.objects.get(
            seat_number=booking.seat_number, room_id=booking.room_id)
        booking.room_id.booked_seats.remove(seat)

        seat_booked_string = str(booking.start_time) + " - " + str(booking.end_time)

        # remove the seat_booked_string from the seat's booked_dates string
        seat.booked_dates = seat.booked_dates.replace(seat_booked_string, "")

        # iif the first two characters in the string are a comma and a space, remove them
        if seat.booked_dates[0:2] == ", ":
            seat.booked_dates = seat.booked_dates[2:]

        seat.save()

        booking.room_id.save()
        booking.delete()
    return redirect("/upcoming")

def send_email(request, bookingid, status="confirmed"):
    booking = Booking.objects.get(id=bookingid)
    if booking is None:
        return redirect("/upcoming")
    else:
        if status == "verified":
            send_verified_email(
                recipient_name=booking.user_id.first_name + " " + booking.user_id.last_name,
                recipient_email=[booking.user_id.email],
                booking_id=booking.id,
                seat=booking.seat_number,
                room=booking.room_id.id,
                building=booking.room_id.building,
                campus=booking.room_id.campus_choice,
                start_time=booking.start_time,
                end_time=booking.end_time,
                status=status,
            )

        else:
        # use the send_booking_email function to send an email to the user
            send_booking_email(
                recipient_name=booking.user_id.first_name + " " + booking.user_id.last_name,
                # recipient_email=["adamgray8432@gmail.com"],
                recipient_email=[booking.user_id.email],
                # recipient_email=["scottcsbrady@icloud.com"],
                booking_id=booking.id,
                seat=booking.seat_number,
                room=booking.room_id.id,
                building=booking.room_id.building,
                campus=booking.room_id.campus_choice,
                start_time=booking.start_time,
                end_time=booking.end_time,
                status=status,
            )
    return redirect("/upcoming")


@login_required
def display_booking_details(request, bookingid):
    booking = Booking.objects.get(id=bookingid)
    if booking is None:
        return redirect("/upcoming")
    else:
        # return the seat number associated with the booking
        return JsonResponse({
            'seat': booking.seat_number,
            'room': booking.room_id.id,
            'is_verified': booking.is_verified,
        })


@login_required
def verify_booking(request, bookingid):
    booking = Booking.objects.get(id=bookingid)
    if booking is None:
        return redirect("/upcoming")
    else:
        #    display all the upcoming bookings for the user
        booking.is_verified = True
        booking.save()
        send_email(request, bookingid, "verified")
        return upcoming_bookings(request)


@login_required
def booking(request):
    user = request.user
    basket = Basket.objects.filter(user_id=user, is_active=True).first()
    # get the room object from the basket item
    room = Room.objects.get(id=basket.basketitem_set.first().room_id.id)
    # get the seat number from the basket item
    seat_number = basket.basketitem_set.first().seat_number
    sbi = BasketItem.objects.filter(basket_id=basket)

    # get the room's booked_seats
    booked_seats = room.booked_seats.all()

    # get the start time and end time from the basket item
    start_time = sbi[0].start_time
    end_time = sbi[0].end_time
    seat_number = sbi[0].seat_number

    seat, created = Seat.objects.get_or_create(
        seat_number=seat_number,
        room_id=room,
        defaults={
            'occupant_first_name': user.first_name,
            'occupant_last_name': user.last_name,
            'occupant_email': user.email,
        }
    )

    if created:
        # if the seat was created, update the occupant details
        seat.occupant_first_name = user.first_name
        seat.occupant_last_name = user.last_name
        seat.occupant_email = user.email
        seat.save()

    if request.method == "POST":
        form = BookingForm(request.POST)
        # check if the form is valid and the name matches the user's name
        if form.is_valid() and form.cleaned_data['name'] == user.first_name + " " + user.last_name:

            booking = form.save(commit=False)
            booking.user_id = user
            booking.basket_id = basket
            booking.name = user.first_name + " " + user.last_name
            booking.room_id = sbi[0].room_id
            booking.start_time = start_time
            booking.end_time = end_time
            booking.seat_number = seat_number

            booking.save()
            basket.is_active = False
            basket.save()

            # get the seat object associated with the booking
            seat = Seat.objects.get(seat_number=booking.seat_number, room_id=booking.room_id)

            # add the booking's start time and end time to the seat's booked_dates field
            seat.booked_dates = seat.booked_dates + str(booking.start_time) + " - " + str(booking.end_time) + ", "
            seat.save()

            # add the seat to the room's booked_seats list
            room.booked_seats.add(seat)
            room.save()

            send_email(request, booking.id, "confirmed")

            return render(request, 'booking_complete.html', {'booking': booking, 'sbi': sbi, 'basket': basket})
        elif not form.cleaned_data['name'] == user.first_name + " " + user.last_name:
            return render(request, 'bookingform.html', {'form': form, 'sbi': sbi, 'basket': basket, 'error': True})
    else:
        form = BookingForm()
        return render(request, 'bookingform.html', {'form': form, 'sbi': sbi, 'basket': basket, 'error': False})


@login_required 
def test_selection(request):
    rooms = Room.objects.all()
    return render(request, 'test-seat.html', {'rooms': rooms})

@csrf_exempt
def occupiedSeats(request):
    data = json.loads(request.body)

    room_id = data['room_id']
    room = Room.objects.get(id=room_id)
    occupied = []

    for seat in room.booked_seats.all():
        for booked_date in seat.booked_dates.split(","):
            # as long as the booked date is not empty
            if booked_date and "-" in booked_date:
                booking_start_str, booking_end_str = booked_date.split(" - ")

                booking_start_str = booking_start_str[:-6].lstrip() # remove +00:00 timezone offset
                booking_end_str = booking_end_str[:-6].lstrip()

                booking_start = datetime.strptime(booking_start_str, "%Y-%m-%d %H:%M:%S")
                booking_end = datetime.strptime(booking_end_str, "%Y-%m-%d %H:%M:%S")
                start_time = datetime.strptime(data['combinedStartTime'], "%Y-%b-%d %H:%M:%S")
                end_time = datetime.strptime(data['combinedEndTime'], "%Y-%b-%d %H:%M:%S")

                if booking_start <= end_time and booking_end >= start_time:
                    occupied.append(seat)
                    break

    occupied_seat = list(map(lambda seat: seat.seat_number - 1, occupied))
    return JsonResponse({
        'occupied_seats': occupied_seat,
        'room': str(room)
    })




@csrf_exempt
def dynamic_seat_selection(request):
    data = json.loads(request.body)
    room = Room.objects.get(id=data['room_id'])
    numRows = room.rows
    numSeats = room.seats
    capacity = room.capacity 

    return JsonResponse({
        'numRows': numRows,
        'numSeats': numSeats,
        'capacity': capacity,
    })

def help(request):
    return render(request, 'help.html')
