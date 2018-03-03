import os
import shutil

from django.core.management.base import BaseCommand

from viewer.models import Song, CHORDTABS_NEW_DIR, CHORDTABS_OLD_DIR


class Command(BaseCommand):
    def handle(self, *args, **options):
        _all = Song.objects.all().values_list('chord_image', flat=True)
        for path in _all:
            path = os.path.join(CHORDTABS_NEW_DIR, path)
            condition = not os.path.isfile(path) or os.stat(path).st_size < 10000
            if condition:
                afile = os.path.basename(path)
                oldpath = os.path.join(CHORDTABS_OLD_DIR, 'c' + afile)
                if os.path.isfile(oldpath):
                    print(path, oldpath)
                    shutil.copyfile(oldpath, path)
