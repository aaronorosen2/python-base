from django.core.management.base import BaseCommand
import subprocess
from ...models import SSIDReading
from ...serializers import  WifiNetworkSerializer
import os

def runIwList():
    try:
        # Setting path for laptop_iwlist_output file  start
        module_dir = os.path.dirname(__file__)  
        file_path = os.path.abspath(os.path.join(module_dir,'..','..', 'laptop_iwlist_output'))   #full path to laptop_iwlist_output.
        # Setting path for laptop_iwlist_output file  end

        # Reading file line by line start
        data_file = open(file_path , 'r')       
        Lines = data_file.readlines()
        # Strips the newline character
        laptop_iwlist_output = [] 
        network_dict = {}
        # Iterating over each line of file 
        for line in Lines:
            # Removing extra white space from file 
            line = line.strip() 
            # Checking that new network is listed in current line 
            if line.startswith('Cell'):
                if len(network_dict) != 0 : 
                    laptop_iwlist_output.append(network_dict)
                    network_dict = {}
                network_dict = {'address' : '','channel' : '', 'frequency' : '', 'quality' : '', 'signal_level' : '','encryption_key' : '', 'essID' : '','bit_rates' : '', "mode" : ''}
            
            # Checking that adress is existing in current line 
            if "Address:" in line :
                network_dict['address'] = line.split("Address:",1)[1]

            # Checking that Channel is existing in current line 
            elif "Channel:" in line :
                network_dict['channel'] = line.split("Channel:",1)[1]

            # Checking that Frequency is existing in current line 
            elif "Frequency:" in line :
                network_dict['frequency'] = line.split("Frequency:",1)[1]

            # Checking that quality is existing in current line 
            elif "Quality=" in line :
                network_quality= line.split("Quality=",1)[1]
                network_dict['quality']  = network_quality.split(" ")[0]

                # Checking that signal evel is existing in current line 
                if "Signal level=" in line :
                    network_dict['signal_level'] = line.split("Signal level=",1)[1]

            # Checking that encryption key is existing in current line 
            elif "Encryption key:" in line :
                network_dict['encryption_key'] = line.split("Encryption key:",1)[1]

            # Checking that essID is existing in current line 
            elif "ESSID:" in line :
                network_dict['essID'] = line.split("ESSID:",1)[1]

            # Checking that bit rates is existing in current line 
            elif "Bit Rates:" in line :
                network_dict['bit_rates'] = line.split("Bit Rates:",1)[1]

            # Checking that mode is existing in current line 
            elif "Mode:" in line :
                network_dict['mode'] = line.split("Mode:",1)[1]

        # Setting data for wifi network serializer
        serializer = WifiNetworkSerializer(data=laptop_iwlist_output,many=True)
        # Throw error if any validtion false for serializer
        serializer.is_valid(raise_exception=True)
        if serializer.is_valid():
            # Inserting the data 
            serializer.save() 
    except Exception as e:
        print(e)


class Command(BaseCommand):
    help = 'fetch and parse iwlist'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):

        # read file laptop_iwlist_output and parse

        # output = subprocess.run(
        #     ["sudo", "iwlist", "scann"], capture_output=True
        # )
        # print(output)
        runIwList()


