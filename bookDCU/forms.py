'''Forms used throughout the application.'''

from datetime import datetime

from django import forms
from django.forms import ModelForm

from .models import Booking

# BookingForm used to create a booking
class BookingForm(ModelForm):
    # The name of the user who created the booking
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Name...'}))

    # Meta class to define the model and fields used
    class Meta:
        model = Booking
        fields = ['name']

# DateTimeForm used to select a date and time on the homepage
class DateTimeForm(forms.Form):
    # The date and time of the booking
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    # functin to check if the date and time is valid
    def clean(self):
        # Call the parent clean function
        cleaned_data = super().clean()

        # Get the current date and time
        current_datetime = datetime.now()

        # Get the selected date and time by combining the date and time fields
        selected_datetime = datetime.combine(cleaned_data['date'], cleaned_data['start_time'])

        # Check if the selected date and time is in the past
        if selected_datetime < current_datetime:
            self.add_error('date', "Date and time must be after the current date and time.")

        # Check if the end time is before the start time
        if cleaned_data['end_time'] <= cleaned_data['start_time']:
            self.add_error('end_time', "End time must be after the start time.")

        return cleaned_data
