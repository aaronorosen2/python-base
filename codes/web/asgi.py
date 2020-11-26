
import django
from channels.http import AsgiHandler
from channels.routing import get_default_application
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'web.settings')
django.setup()

application = get_default_application()