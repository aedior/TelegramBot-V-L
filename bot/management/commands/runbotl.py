from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "start telegram bot"

    def handle(self, *args, **options):
        import bot.mainL
        