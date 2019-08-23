import os

from django.core.management import BaseCommand, call_command


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        os.chdir('vue')
        os.system("npm run build")
        os.chdir('..')
        call_command(
            'collectstatic',
            '-c',
            '--no-input',
        )
