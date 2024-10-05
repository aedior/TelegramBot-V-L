from django.core.management.base import BaseCommand
from os import system
import time
class Command(BaseCommand):
    help = "start telegram bot"

    def handle(self, *args, **options):
        while True:
            time.sleep(2)
            system("git add .")
            system("git commit -a -m 'db update'")
            system("git push")
        