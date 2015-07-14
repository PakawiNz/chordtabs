# -*- utf-8 -*-
from django.shortcuts import render,redirect
import urllib2,re,threading,Queue

from .models import User,Song,View,models

CHORDTABS_CRD_URL = 'http://chordtabs.in.th/%s'
# CHORDTABS_IMG_URL = 'http://chordtabs.in.th/admin/admin/songsxx/%s.png'
CHORDTABS_IMG_URL = 'http://chordtabs.in.th/song.php?song_id=%s&chord=yes'
CHORDTABS_SRC_URL = 'http://chordtabs.in.th/%E0%B8%84%E0%B8%AD%E0%B8%A3%E0%B9%8C%E0%B8%94%E0%B9%80%E0%B8%9E%E0%B8%A5%E0%B8%87.php'
# Create your views here.

def get_user(request):
	try :
		return User.objects.get(id=request.session['user'])
	except :
		return None

def _download(q,song):
	try :
		result = find_chord_image(song)
		print result
	except Exception as e :
		result = None
		q.put(song)
		print e

def download_all():
	songs = Song.objects.filter(chord_image="").values_list('code',flat=True)
	q = Queue.Queue()
	for song in songs :
		_download(q, song)

	while not q.empty():
		_download(q,q.get())

def refresh(request):

	print "GET CHORD IMAGE URL"
	download_all()
	return redirect('/')	

	f = urllib2.urlopen(urllib2.Request(url=CHORDTABS_SRC_URL))
	temp = f.read()
	print "GOT SOURCE HTML PAGE"

	# tempfile = open('noob.txt','r')
	# tempfile.write(temp)
	# temp = tempfile.read()
	# tempfile.close()

	allsong = re.findall(r'<a\s+href="[^"]+=(\d+)".*title=\'(.*)\'', temp)
	print "GOT SOURCE %d SONGS"%(len(allsong))

	songs = []
	codes = set(Song.objects.values_list('code',flat=True))
	for sid,desc in allsong :
		if int(sid) in codes :
			continue
		songs.append(Song(code=sid,description=desc))
		
	print "CREATE NEW %d SONGS"%(len(songs))
	Song.objects.bulk_create(songs)

	return redirect('/')	

def find_chord_image(song__code):
	song = Song.objects.get(code=song__code)

	if not song.chord_url :
		html = urllib2.urlopen(urllib2.Request(url=CHORDTABS_IMG_URL%song__code)).read()
		match = re.search(r'id="songMain"[^.]*?img src="([^"]*)"', html)
		if match : 
			song.chord_url = CHORDTABS_CRD_URL%(match.group(1)[2:])
			song.save()
		else :
			return ""

	# return song.chord_url
	if not song.chord_image :
		song.get_remote_chord()

	return "/media/%s"%(song.chord_image)

def get_context(request):
	context = {}
	context['user'] = User.objects.filter(pk=request.session.get('user')).first()
	return context

def login(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = User.objects.filter(username=username,password=password)
	if user :
		request.session['user'] = user.first().id
	else :
		pass
	return redirect(request.META['HTTP_REFERER'])

def logout(request):
	request.session.clear()
	return redirect(request.META['HTTP_REFERER'])

def set_favorite(request,song):
	song = Song.objects.get(code=song)
	user = User.objects.get(id=request.session['user'])
	view = View.objects.get_or_create(song=song,user=user)[0]
	view.isFavorite = True
	view.save()
	return redirect(request.META['HTTP_REFERER'])

def unset_favorite(request,song):
	song = Song.objects.get(code=song)
	user = User.objects.get(id=request.session['user'])
	view = View.objects.get_or_create(song=song,user=user)[0]
	view.isFavorite = False
	view.save()
	return redirect(request.META['HTTP_REFERER'])

def view_chord(request,song):
	song = Song.objects.get(code=song)
	user = User.objects.get(id=request.session['user'])
	view = View.objects.get_or_create(song=song,user=user)[0]
	view.count += 1
	view.save()
	chord = find_chord_image(song.code)
	# return redirect(CHORDTABS_IMG_URL%song.code)
	# return redirect(request.META['HTTP_REFERER'])
	context = get_context(request)
	context['code'] = song.code
	context['favorite'] = view.isFavorite
	context['chord'] = chord
	return render(request,"chord.html",context)

def favorite(request):
	user = get_user(request)
	if user == None :
		return redirect('/')

	views = View.objects.filter(user=user,isFavorite=True).order_by('-count','song__description')
	views = list(views.values('song__code','song__description','count','isFavorite'))

	result = []
	for view in views :
		song = {}
		song['code'] = view['song__code']
		song['description'] = view['song__description']
		song['view'] = view['count']
		song['favorite'] = view['isFavorite']
		result.append(song)

	context = get_context(request)
	context['songs'] = result
	return render(request,"search.html",context)

def search(request):
	keyword = request.GET.get('keyword')

	user = get_user(request)
	songs = Song.objects.filter(
			description__icontains=keyword,
		).values('id')
	views = View.objects.filter(song__in=songs,user=user).order_by('-count','song__description')
	songs = songs.exclude(id__in=views.values('song')).order_by('description')

	views = list(views.values('song__code','song__description','count','isFavorite'))
	songs = list(songs.values('code','description'))

	result = []
	for view in views :
		song = {}
		song['code'] = view['song__code']
		song['description'] = view['song__description']
		song['view'] = view['count']
		song['favorite'] = view['isFavorite']
		result.append(song)

	for song in songs :
		song['view'] = 0
		result.append(song)

	context = get_context(request)
	context['songs'] = result
	return render(request,"search.html",context)

def homepage(request):
	user = get_user(request)

	if user :
		views = View.objects.filter(user=user).order_by('-count','song__description')
		views = list(views.values('song__code','song__description','count','isFavorite')[:10])

		result = []
		for view in views :
			song = {}
			song['code'] = view['song__code']
			song['description'] = view['song__description']
			song['view'] = view['count']
			song['favorite'] = view['isFavorite']
			result.append(song)

		context = get_context(request)
		context['mostviews'] = filter(lambda x: x['favorite'] == False ,result)
		context['recentviews'] = filter(lambda x: x['favorite'] == True ,result)
	else :
		context = get_context(request)

	return render(request,"index.html",context)
