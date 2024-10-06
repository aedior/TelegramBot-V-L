from django.core.management.base import BaseCommand
from os import system
import time
class Command(BaseCommand):
    help = "start telegram bot"

    def handle(self, *args, **options):
        print("commit start..")
        while True:
            system("git add . -A")
            system("git commit -a -m 'db update'")
            system("git push")
            time.sleep(21600)
        