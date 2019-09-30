import os, sys, csv
from datetime import date

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "documenter.settings")

import django
import lorem
django.setup()

from rate_doc.models import * 
from django.contrib.auth.models import User

for i in range(100):

    report = Report(
        title = lorem.sentence(),
        section = "Section",
        page = 3,
        report_text_html = lorem.text(),
        )

    report.save()

    for user in User.objects.all():
        doc = Doc(
            assignedTo = user,
            report = report,
            )
        doc.save()
