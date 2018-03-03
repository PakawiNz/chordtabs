import urllib.request
import re

from viewer.models import Song

CHORDTABS_CRD_URL = 'http://chordtabs.in.th/%s'
CHORDTABS_IMG_URL = 'http://chordtabs.in.th/song.php?song_id=%s&chord=yes'
CHORDTABS_SRC_URL = 'http://chordtabs.in.th/%E0%B8%84%E0%B8%AD%E0%B8%A3%E0%B9%8C%E0%B8%94'

# LINK_FORMAT = r'<a\s+href="[^"]+=(\d+)".*title=\'(.*)\''
LINK_FORMAT = r'href="[^"]+-(\d+)\.html".*title=\'(.*)\''


def find_chord_image(song__code):
    song = Song.objects.get(code=song__code)

    if not song.chord_url:

        with urllib.request.urlopen(CHORDTABS_IMG_URL % song__code) as url:
            html = url.read().decode('utf-8')

        match = re.search(r'id="songMain"[^.]*?img src="([^"]*)"', html)
        if match:
            song.chord_url = CHORDTABS_CRD_URL % (match.group(1)[2:])
            song.save()
        else:
            return ""

    # return song.chord_url
    if not song.chord_image:
        song.get_remote_chord()

    return "/media/%s" % song.chord_image
