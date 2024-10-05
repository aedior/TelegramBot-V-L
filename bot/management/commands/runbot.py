from django.core.management.base import BaseCommand
from subprocess import Popen


class Command(BaseCommand):
    help = "start telegram bot"

    def handle(self, *args, **options):
        Popen("python ./manage.py runbotl")
        Popen("python ./manage.py runbotv")
        Popen("python ./manage.py commitdata")
        