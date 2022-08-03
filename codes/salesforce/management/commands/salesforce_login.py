import os
from django.core.management.base import BaseCommand

from utils.browser import init_driver



class Command(BaseCommand):
    help = 'Import address extra'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        print("here is the start")
        driver = init_driver("firefox")
        driver.get("https://na46.test1.pc-rnd.salesforce.com/")
        driver.find_element_by_css_selector("#username").send_keys(
            "tal2_designer1@na46.com")
        driver.find_element_by_css_selector("#password").send_keys(
            "test1234")
        driver.find_element_by_css_selector("#Login").click()
