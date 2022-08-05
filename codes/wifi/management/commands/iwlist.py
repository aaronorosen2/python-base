from django.core.management.base import BaseCommand
from wifi.models import SSIDReading
import os
from utils import wifi


def wifi_scan(training_label):

    ssids = wifi.scan_networks()
    # now we save all the ssid's to SSIDReading
    for ssid in ssids:
        print(ssid)
        ssid_reading = SSIDReading()
        ssid_reading.address = ssid['address']
        ssid_reading.channel = ssid['channel']
        ssid_reading.quality = ssid['quality']
        ssid_reading.signal_level = ssid['signal_level']
        ssid_reading.training_label = training_label
        ssid_reading.save()


class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        wifi_scan("Starbucks_Palo_Alto")
