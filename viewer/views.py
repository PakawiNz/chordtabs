# -*- utf-8 -*-
from django.shortcuts import render,redirect
import urllib2,re

from .models import User,Song,View,models

# CHORDTABS_IMG_URL = 'http://chordtabs.in.th/admin/admin/songsxx/%s.png'
CHORDTABS_IMG_URL = 'http://chordtabs.in.th/song.php?song_id=%s&chord=yes'
CHORDTABS_SRC_URL = 'http://chordtabs.in.th/%E0%B8%84%E0%B8%AD%E0%B8%A3%E0%B9%8C%E0%B8%94%E0%B9%80%E0%B8%9E%E0%B8%A5%E0%B8%87.php'
# Create your views here.

def get_user(request):
	try :
		return User.objects.get(id=request.session['user'])
	except :
		return None

def refresh(request):
	# tempfile = open('noob.txt','w')
	# f = urllib2.urlopen(urllib2.Request(url=CHORDTABS_SRC_URL)) 
	# f = urllib2.urlopen(urllib2.Request(url=CHORDTABS_SRC_URL)) 
	# tempfile.write(f.read())
	tempfile = open('noob.txt','r')
	temp = tempfile.read()
	allsong = re.findall(r'<a\s+href="[^"]+=(\d+)".*title=\'(.*)\'', temp)

	songs = []
	codes = set(Song.objects.values_list('code',flat=True))
	for sid,desc in allsong :
		if int(sid) in codes :
			continue
		songs.append(Song(code=sid,description=desc))
	Song.objects.bulk_create(songs)

	tempfile.close()
	return render(request,"index.html",get_context(request))	

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
	return redirect(CHORDTABS_IMG_URL%song.code)

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
