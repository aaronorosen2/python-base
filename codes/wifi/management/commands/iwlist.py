from django.core.management.base import BaseCommand
from wifi.models import SSIDReading
import os
from utils import wifi
import platform


def wifi_scan(training_label):
    sys_os = platform.system()

    # now we save all the ssid's to SSIDReading
    if sys_os == 'Linux':
        ssids = wifi.scan_networks()
        for ssid in ssids:
            print(ssid)
            ssid_reading = SSIDReading()
            ssid_reading.address = ssid['address']
            ssid_reading.channel = ssid['channel']
            ssid_reading.quality = ssid['quality']
            ssid_reading.signal_level = ssid['signal_level']
            ssid_reading.training_label = training_label
            ssid_reading.save()
    if sys_os == 'Windows':
        ssids = wifi.scan_networks()
        size_loop = len(ssids)
        for i in range(size_loop):
            ssid_reading = SSIDReading()
            data_network = ssids['connection'+str(i)]
            ssid_reading.address = data_network['BSSID 1']
            ssid_reading.channel = data_network['Channel']
            ssid_reading.quality = data_network['Signal']
            #ssid_reading.signal_level = data_network['address']
            ssid_reading.training_label = training_label
            ssid_reading.save()


class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        wifi_scan("Starbucks_Palo_Alto")
