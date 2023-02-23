from django.db import models
from django.contrib.auth.models import AbstractUser

# Class to represent a user
class APIUser(AbstractUser):
    pass

# Class to represent a room
class Room(models.Model):

    GLASNEVIN = 'GLA'
    STPATS = 'SPD'
    ALLHALLOWS = 'AHC'

    # The campus the room is in
    CAMPUS_CHOICES = [
        (GLASNEVIN, 'Glasnevin Campus'),
        (STPATS, 'St Pats Campus'),
        (ALLHALLOWS, 'All Hallows Campus')
    ]
    
    campus = models.CharField(
        max_length = 4,
        choices = CAMPUS_CHOICES,
        default=GLASNEVIN
    )

    # The room id, e.g. L1.29
    id = models.CharField(max_length=5, null=False, primary_key=True)

    building = models.CharField(max_length = 200, null=False)

    # The number of seats in the room
    capacity = models.IntegerField(null=False)

    # Seats that have been booked for this room
    booked_seats = models.ManyToManyField('Seat', blank="True")

    # The date the room was created
    created = models.DateTimeField(auto_now_add=True)

    # The number of rows in the room
    rows = models.IntegerField(null=False)

    # The number of seats in each row
    seats = models.IntegerField(null=False)

    # Function to return the campus name
    def campus_choice(self):
        return [x[1] for x in self.CAMPUS_CHOICES if self.campus == x[0]][0]

    # Function to return the room id
    def __str__(self):
        return f"{self.id}"

# Class to represent a basket containing bookings
class Basket(models.Model):
    # The id of the basket
    id = models.AutoField(primary_key=True)

    # The user who created the basket
    user_id = models.ForeignKey(APIUser, on_delete=models.CASCADE)

    # Whether the basket is active
    is_active = models.BooleanField(default=True)

    # The date the basket was created
    date_created = models.DateTimeField(auto_now_add=True)

# Class to represent a booking in a basket
class BasketItem(models.Model):
    # The id of the basket item
    id = models.AutoField(primary_key=True)

    # The date the basket item was created    
    date_created = models.DateTimeField(auto_now_add=True)

    # The basket the basket item is in
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)

    # The user who created the basket item
    user_id = models.ForeignKey(APIUser, on_delete=models.CASCADE)

    # The name of the yser who created the basket item
    name = models.TextField(default="")

    # The room attached to the basket item
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, default='L1.29')

    # The start time of the booking
    start_time = models.DateTimeField(null=False)

    # The end time of the booking
    end_time = models.DateTimeField(null=False)

    # The seat number of the booking
    seat_number = models.IntegerField(null=False, default=1)

    # Whether the basket item is active
    is_active = models.BooleanField(default=True)

# Class to represent a booking
class Booking(models.Model):
    # The id of the booking
    id = models.AutoField(primary_key=True)

    # The date the booking was created
    date_booked = models.DateTimeField(auto_now_add=True)

    # The basket the booking is in
    basket_id = models.ForeignKey(Basket, on_delete=models.CASCADE)

    # The user who created the booking
    user_id = models.ForeignKey(APIUser, on_delete=models.CASCADE)

    # The name of the user who created the booking
    name = models.TextField(default="")

    # The room the booking is for
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, default=1)

    # The start time of the booking
    start_time = models.DateTimeField(null=False, default='2023-02-20 14:30:00')

    # The end time of the booking
    end_time = models.DateTimeField(null=False, default='2023-02-20 16:30:00')

    # The seat number of the booking
    seat_number = models.IntegerField(null=False, default=1)

    # Whether the booking is active
    is_active = models.BooleanField(default=True)

    # Whether the booking is verified
    is_verified = models.BooleanField(default=False)

# Class to represent a seat
class Seat(models.Model):
    # The id of the seat
    id = models.AutoField(primary_key=True)
    
    # The room the seat is in
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE)
    
    # The seat number
    seat_number = models.IntegerField()

    # Whether the seat is booked or not
    # is_booked = models.BooleanField(default=True)

    # create a field that can store all of the dates and times that the seat is booked
    booked_dates = models.TextField(default="")
    
    # The date the seat was booked
    book_time = models.DateTimeField(auto_now_add=True)

    # The first name of the occupant
    occupant_first_name = models.CharField(max_length=200)

    # The last name of the occupant
    occupant_last_name = models.CharField(max_length=200)

    # The email of the occupant
    occupant_email = models.EmailField(max_length=200)
    
    # Function to return the name and seat number of the occupant
    def __str__(self):
        return f"{self.occupant_first_name}-{self.occupant_last_name} seat_number: {self.seat_number}"

    