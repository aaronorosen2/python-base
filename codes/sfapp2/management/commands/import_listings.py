import pandas as pd
from django.core.management.base import BaseCommand

from sfapp2.models import Service


class Command(BaseCommand):
    help = 'Crawl Agent Links'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        df = pd.read_csv("help_data.csv")
        print(df)
        for i in df.iloc:
            service = Service.objects.filter(url=i.url).first()
            if not service:
                service = Service()
            try:
                if i.phone and 'tel' in i.phone:
                    print(i.phone)
                    print(len(i.phone))
                    service.phone = i.phone
            except TypeError:
                pass
            service.url = i.url
            service.title = i.title
            service.description = i.description
            service.phone = i.phone
            service.address = i.address
            service.latitude = i.lat
            service.longitude = i.long
            service.services = i.services
            service.other_info = i.other_info
            service.services_list = i.services_list
            service.population_list = i.population_list
            service.save()
