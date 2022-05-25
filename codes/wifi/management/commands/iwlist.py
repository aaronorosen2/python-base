from django.core.management.base import BaseCommand
import subprocess


class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        # read file laptop_iwlist_output and parse

        output = subprocess.run(
            ["sudo", "iwlist", "scann"], capture_output=True
        )
        print(output)
        # XXX need to now parse output and format results like:
        # parse Cell
        # {"Address": "10:8E:BA:04:54:05",
        #   "Channel": 1...



#          Cell 14 - Address: 10:8E:BA:04:54:05
#                    Channel:1
#                    Frequency:2.412 GHz (Channel 1)
#                    Quality=45/70  Signal level=-65 dBm  
#                    Encryption key:on
#                    ESSID:""
#                    Bit Rates:1 Mb/s; 2 Mb/s; 5.5 Mb/s; 11 Mb/s; 6 Mb/s
#                              9 Mb/s; 12 Mb/s; 18 Mb/s
#                    Bit Rates:24 Mb/s; 36 Mb/s; 48 Mb/s; 54 Mb/s
#                    Mode:Master
#                    Extra:tsf=000003c5116111be
#                    Extra: Last beacon: 4172ms ago
#                    IE: Unknown: 0000
#                    IE: Unknown: 010882848B960C121824
#                    IE: Unknown: 030101
#                    IE: Unknown: 050400010000
#                    IE: Unknown: 0706555320010B14
#                    IE: Unknown: 2A0100
#                    IE: Unknown: 2D1A2C0100FF00000000000000000000000000000000000000000000
#                    IE: IEEE 802.11i/WPA2 Version 1
#                        Group Cipher : CCMP
#                        Pairwise Ciphers (1) : CCMP
#                        Authentication Suites (1) : PSK
#                    IE: Unknown: 32043048606C
#                    IE: Unknown: 3D1601080000000000000000000000000000000000000000
#                    IE: Unknown: DD180050F2020101000003A4000027A4000042435E0062322F00


