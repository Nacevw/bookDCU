from django.core.management.base import BaseCommand
from bookDCU.models import *
from django.contrib.sites.models import Site

# import allauth models
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider

""" Clear all data and creates addresses """
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

# Class to seed the database
class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def populate_rooms():
    # delete old details
    Booking.objects.all().delete() # I imagine booking has a fk to room, so bookings must be deleted before rooms can
    Room.objects.all().delete()
    Room.objects.create(id="L1.28", campus='GLA', building='McNulty', capacity=60, rows=10, seats=6)
    Room.objects.create(id="L1.29", campus='GLA', building='McNulty', capacity=36, rows=6, seats=6)
    Room.objects.create(id="LG.26", campus='GLA', building='McNulty', capacity=54, rows=9, seats=6)
    Room.objects.create(id="Laptop Bar", campus='GLA', building='McNulty', capacity=7, rows=1, seats=7)

def populate_social_app():
    # delete old details
    SocialApp.objects.all().delete()

    # create a social app
    SocialApp.objects.create(
        provider=GoogleProvider.id,
        name='bookDCU',
        client_id='85703386568-198tvo18q7r5ag0vh71ldecponauvfb1.apps.googleusercontent.com',
        secret='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',
    )
    # create a site
    site = Site.objects.create(domain='127.0.0.1:8000', name='127.0.0.1:8000')
    site.save()
    
    # # add the site to the social app
    social_app = SocialApp.objects.get(provider=GoogleProvider.id)
    social_app.sites.add(site)


# Function to seed the database
def run_seed(self, mode):
    """ Seed database based on mode
    :param mode: refresh / clear
    :return:
    """
    APIUser.objects.create_user('TestAccount','scottbradyapps@gmail.com','AppleTree')


    APIUser.objects.create_superuser('admin', 'admin@example.com', 'pass')
    populate_rooms()
    populate_social_app()
