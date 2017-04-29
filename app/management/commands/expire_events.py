from django.core.management.base import BaseCommand
import datetime
from app.models import Rides
class Command(BaseCommand):

    help = 'Expires event objects which are out-of-date'

    def handle(self, *args, **options):
        Rides.objects.filter(date_time__lt=datetime.datetime.now()).delete()