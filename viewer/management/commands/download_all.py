import queue
import threading

from django.core.management.base import BaseCommand

from viewer.models import Song
from viewer.utils import find_chord_image


def _download(q, song):
    try:
        result = find_chord_image(song)
        print(result)
    except Exception as e:
        q.put(song)
        print(e)


class Command(BaseCommand):
    def handle(self, *args, **options):
        print("FILTER CHORD IMAGE URL")

        songs = Song.objects.filter(chord_image="").values_list('code', flat=True)
        songs = list(songs)
        print("DOWNLOADING %s CHORDS" % (len(songs)))

        q = queue.Queue()
        for song in songs:
            q.put(song)

        print("BEGIN DOWNLOAD")

        def interval():
            if not q.empty():
                threading.Timer(0.1, interval).start()
                _download(q, q.get())

        interval()
