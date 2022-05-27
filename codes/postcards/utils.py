import requests


def send_request(first_name, address_line1, city, zip_code, country='US'):
    url = 'https://api.postgrid.com/print-mail/v1/postcards'
    headers = {
        'x-api-key': 'live_sk_knKQKkKXrT8i8ZtBGQaj16'
    }

    data = {
        'to[firstName]': first_name,
        'to[addressLine1]': address_line1,
        'to[city]': city,
        'to[postalOrZip]': zip_code,
        'to[country]': country,
        'size': '6x4',
        'frontTemplate': 'template_gQkz8iMqHLDXH8Ch9AFE7R',
        'backTemplate': 'template_uPxaUnX1Z3jtKbEp1JipEL',
        'mergeVariables[LOGO]': 'https://agentstat.com/img/logo-beta.png'
    }

    response = requests.post(url, headers=headers, data=data)
    return response.json()


def delete_postcard(post_card_id):
    url = 'https://api.postgrid.com/print-mail/v1/postcards/%s' % post_card_id
    headers = {
        'x-api-key': 'live_sk_knKQKkKXrT8i8ZtBGQaj16'
    }

    response = requests.delete(url, headers=headers)
    return response.json()
