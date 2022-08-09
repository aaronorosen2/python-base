import os
import platform
from subprocess import check_output


def scan_networks():
    os_platform = platform.system()
    if os_platform == 'Linux':
        return scan_wifi_linux()
    elif os_platform == 'Windows':
        return scan_wifi_windows()


def scan_wifi_linux():
    os.system("sudo iwlist scann > /tmp/iwlist_output")
    file_path = '/tmp/iwlist_output'

    # Reading file line by line start
    data_file = open(file_path, 'r')
    Lines = data_file.readlines()
    # Strips the newline character
    ssids = []
    network_dict = {}
    # Iterating over each line of file
    for line in Lines:
        # Removing extra white space from file
        line = line.strip()

        # Checking that new network is listed in current line
        if line.startswith('Cell'):
            if len(network_dict) != 0:
                ssids.append(network_dict)
                network_dict = {}
            network_dict = {
                'address': '', 'channel': '', 'frequency': '',
                'quality': '', 'signal_level': '',
                'encryption_key': '', 'essID': '',
                'bit_rates': '', "mode": ''}
        # Checking that adress is existing in current line
        if "Address:" in line:
            network_dict['address'] = line.split("Address:", 1)[1]

        # Checking that Channel is existing in current line
        elif "Channel:" in line:
            network_dict['channel'] = line.split("Channel:", 1)[1]

        # Checking that Frequency is existing in current line
        elif "Frequency:" in line:
            network_dict['frequency'] = line.split("Frequency:", 1)[1]

        # Checking that quality is existing in current line
        elif "Quality=" in line:
            network_quality = line.split("Quality=", 1)[1]
            network_dict['quality'] = network_quality.split(" ")[0]
            quality_percentage = network_dict['quality'].split("/")
            network_dict['quality'] = \
                int(quality_percentage[0])/int(quality_percentage[1])

            print(network_dict['quality'])
            # Checking that signal evel is existing in current line
            if "Signal level=" in line:
                network_dict['signal_level'] = line.split(
                    "Signal level=", 1)[1]

        # Checking that encryption key is existing in current line
        elif "Encryption key:" in line:
            network_dict['encryption_key'] = line.split(
                "Encryption key:", 1)[1]

        # Checking that essID is existing in current line
        elif "ESSID:" in line:
            network_dict['essID'] = line.split("ESSID:", 1)[1]

        # Checking that bit rates is existing in current line
        elif "Bit Rates:" in line:
            network_dict['bit_rates'] = line.split("Bit Rates:", 1)[1]

        # Checking that mode is existing in current line
        elif "Mode:" in line:
            network_dict['mode'] = line.split("Mode:", 1)[1]
    return ssids


def scan_wifi_windows():
    '''
    list of keys follow as:
        1. SSID 10 : home339E
        2. Network type
        3. Authentication
        4. Encryption
        5. BSSID 1
        6 Signal
        7. Radio type
        8. Channel
        9. Basic rates (Mbps)
        10. Other rates (Mbps)

    :return:
        Dictionary of the wifi connections:
    '''

    listWifi = check_output("netsh wlan show networks mode=Bssid", shell=True).decode()
    print(listWifi)
    text_file = open("laptop_iwlist_windows_output.txt", "w")
    n = text_file.write(listWifi)
    count = 0
    text_file.close()
    main_dict = {}
    count_connection = 0
    network_dict = {}
    try:
        from_file = open('laptop_iwlist_windows_output.txt', 'r')
        lines = from_file.readlines()
        # Deleting lines which aren't of use from the executed command
        del lines[0]
        del lines[1]
        del lines[2]

        for line in lines:

            if count == 10:
                count = 0
                main_dict['connection' + str(count_connection)] = network_dict
                count_connection = count_connection + 1
                network_dict = {}
            if line != ' ' and line != '':
                if len(line.split(':')) > 1:
                    # print(line)
                    splited = line.split(':')
                    key, value = splited[0], splited[1]
                    key = key.strip(' ')
                    value = value.lstrip(' ')
                    key = key.rstrip(' ')
                    value = value.replace("\n", "")
                    value = value.rstrip(' ')
                    network_dict[key] = value
                    count = count + 1
    except Exception as e:
        print(e)
    return main_dict
