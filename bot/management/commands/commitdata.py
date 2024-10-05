from django.core.management.base import BaseCommand
from os import system
import time
class Command(BaseCommand):
    help = "start telegram bot"

    def handle(self, *args, **options):
        print("commit start..")
        while True:
            time.sleep(21600)
            system("git add .")
            system("git commit -a -m 'db update'")
            system("git push")
        