import re
import urllib.request

from django.core.management.base import BaseCommand

from viewer.models import Song
from viewer.utils import CHORDTABS_SRC_URL, LINK_FORMAT


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("GET CHORD IMAGE URL")

        with urllib.request.urlopen(CHORDTABS_SRC_URL) as url:
            bytes().decode()
            temp = url.read().decode('utf-8')

        print("GOT SOURCE HTML PAGE")

        temp_file = open('song_index.html', 'w', encoding='utf-8')
        temp_file.write(temp)
        temp_file.close()

        allsong = re.findall(LINK_FORMAT, temp)
        print("GOT SOURCE %d SONGS" % (len(allsong)))

        songs = []
        codes = set(Song.objects.values_list('code', flat=True))
        for sid, desc in allsong:
            if int(sid) in codes:
                continue
            songs.append(Song(code=sid, description=desc))

        print("CREATE NEW %d SONGS" % (len(songs)))
        Song.objects.bulk_create(songs)
