import re
import requests

from django.core.management.base import BaseCommand

from viewer.models import Song
from viewer.utils import CHORDTABS_SRC_URL, LINK_FORMAT


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("GET CHORD IMAGE URL")

        temp = requests.get(CHORDTABS_SRC_URL).text

        print("GOT SOURCE HTML PAGE")

        temp_file = open('song_index.html', 'w', encoding='utf-8')
        temp_file.write(temp)
        temp_file.close()

        allsong = re.findall(LINK_FORMAT, temp)
        print("GOT SOURCE %d SONGS" % (len(allsong)))

        songs = []
        codes = set(Song.objects.values_list('code', flat=True))
        for song_code, description in allsong:
            song_code = int(song_code)
            if song_code in codes:
                continue

            codes.add(song_code)
            song = Song(code=song_code, description=description)
            songs.append(song)

        print("CREATE NEW %d SONGS" % (len(songs)))
        Song.objects.bulk_create(songs)
