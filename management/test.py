#!/usr/bin/env python3

import sys
import os
import django


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["DJANGO_SETTINGS_MODULE"] = "AiPlatform.settings"

django.setup()

from management.models import Event

if __name__ == "__main__":
    events = Event.objects.all()
    print(events)
    print('test success')
