# -*- utf-8 -*-
from django.shortcuts import render,redirect
from django.http import HttpResponse
import simplejson

from django.db.models import Sum,Count
from .models import User,Song,View,Playlist,PlaylistItem
from .utils import find_chord_image

# ==================================================== HELPER

def reload_page(request):
    return redirect(request.META['HTTP_REFERER'])

def invalid_ajax(message):
    return HttpResponse("")

def success_ajax(message):
    return HttpResponse(simplejson.dumps({'success':True}))

def ajax_response(context):
    return HttpResponse(simplejson.dumps(context))

def get_user(request):
    try :
        return User.objects.get(id=request.session['user'])
    except :
        return None

def get_context(request):
    context = {}
    context['user'] = User.objects.filter(pk=request.session.get('user')).first()
    return context

# ==================================================== PLAYLIST AND FAVORITE

def request_song(request,song):

    song = Song.objects.get(code=song)
    playlist = Playlist.objects.get(id=24)

    items = PlaylistItem.objects.filter(song=song,playlist=playlist)
    if not items.exists() :
        PlaylistItem.objects.create(number=items.count()+1,song=song,playlist=playlist)

    return success_ajax('')

def set_favorite(request,song):
    song = Song.objects.get(code=song)
    user = User.objects.get(id=request.session['user'])
    view = View.objects.get_or_create(song=song,user=user)[0]
    view.isFavorite = True
    view.save()
    return success_ajax('')

def unset_favorite(request,song):
    song = Song.objects.get(code=song)
    user = User.objects.get(id=request.session['user'])
    view = View.objects.get_or_create(song=song,user=user)[0]
    view.isFavorite = False
    view.save()
    return success_ajax('')

def get_playlist(request):
    user = get_user(request)
    if not user :
        return ajax_response(context)
    song = Song.objects.get(code=request.POST.get('song'))
    song_in = PlaylistItem.objects.filter(playlist__owner=user,song=song).values_list('playlist',flat=True)
    song_in = set(list(song_in))

    playlists = Playlist.objects.filter(owner=user).values('id','name')
    playlists = list(playlists)
    for playlist in playlists :
        playlist['isin'] = playlist['id'] in song_in

    context = {}
    context['playlists'] = list(playlists)
    return ajax_response(context)

def new_playlist(request):
    user = get_user(request)
    name = request.POST.get('create-playlist-name')
    desc = request.POST.get('create-playlist-desc')

    if not user or len(name) < 4 :
        return invalid_ajax()

    playlist = Playlist(
        owner = user,
        name = name,
        description = desc,
    )
    playlist.save()
    return success_ajax("SUCCESS")

def del_playlist(request,playlist):
    if not get_user(request) :
        return redirect('/')

    playlists = Playlist.objects.filter(owner=get_user(request),pk=playlist)
    playlists.delete()

    return reload_page(request)

def add_to_playlist(request):
    if not get_user(request) :
        return invalid_ajax()

    song = Song.objects.get(code=request.POST.get('song'))
    playlist = Playlist(request.POST.get('playlist'))

    items = PlaylistItem.objects.filter(song=song,playlist=playlist,playlist__owner=get_user(request))
    if not items.exists() :
        PlaylistItem.objects.create(number=items.count()+1,song=song,playlist=playlist)
    else :
        items.delete()

    return success_ajax("SUCCESS")

def view_playlist(request,playlist):
    user = get_user(request)
    if not user : return ajax_response(context)

    playlist = Playlist.objects.get(pk=playlist)

    no_view = PlaylistItem.objects.filter(playlist=playlist)

    items = PlaylistItem.objects.filter(playlist=playlist)

    has_viewed = items.filter(song__views__user=user)
    has_viewed = has_viewed.values('song__code','song__description','song__views__count','song__views__isFavorite')

    not_viewed = items.exclude(pk__in=has_viewed.values('pk'))
    not_viewed = not_viewed.values('song__code','song__description')

    items = list(has_viewed) + list(not_viewed)

    result = []
    for item in items :
        song = {}
        song['code'] = item['song__code']
        song['description'] = item['song__description']
        song['view'] = item.get('song__views__count') or 0
        song['favorite'] = item.get('song__views__isFavorite') or False
        result.append(song)

    context = get_context(request)
    context['songs'] = result
    context['name'] = playlist.name

    return render(request,"playlist_view.html",context)

def playlist(request):
    user = get_user(request)
    if not user : return ajax_response(context)

    playlists = Playlist.objects.filter(owner=user).values('id').annotate(Count('items'))
    playlists = playlists.values('id','name','items__count')

    context = get_context(request)
    context['playlists'] = playlists
    return render(request,"playlist.html",context)

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

# ==================================================== CORE FUNCTION

def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = User.objects.filter(username=username,password=password)
    if user :
        request.session['user'] = user.first().id
    else :
        pass
    return reload_page(request)

def logout(request):
    request.session.clear()
    return reload_page(request)

def view_chord(request,song):
    song = Song.objects.get(code=song)
    user = get_user(request)
    view = View.objects.get_or_create(song=song,user=user)[0]
    view.count += 1
    view.save()
    chord = find_chord_image(song.code)
    context = get_context(request)
    context['code'] = song.code
    context['favorite'] = view.isFavorite
    context['chord'] = chord
    return render(request,"chord.html",context)

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

    # views = View.objects.values('song').annotate(sum_count=Sum('count')).order_by('-sum_count','song__description').select_related('song')
    songs = Song.objects.filter(views__count__gt=0)
    songs = songs.annotate(sum_count=Sum('views__count'))
    songs = songs.order_by('-sum_count','description')
    songs = list(songs[:20])

    song_set = set()
    mostviews = []
    for song in songs :
        row = {}
        row['code'] = song.code
        row['description'] = song.description
        row['view'] = song.sum_count
        if user :
            view = song.views.filter(user=user)
            if view.exists() :
                row['favorite'] = view.get().isFavorite
        else :
            row['favorite'] = False

        song_set.add(song.code)
        mostviews.append(row)

    songs = Song.objects.exclude(code__in=song_set)
    songs = songs.annotate(sum_count=Sum('views__count'))
    songs = songs.order_by('?')
    songs = list(songs[:20])

    randoms = []
    for song in songs :
        row = {}
        row['code'] = song.code
        row['description'] = song.description
        row['view'] = song.sum_count
        if user :
            view = song.views.filter(user=user)
            if view.exists() :
                row['favorite'] = view.get().isFavorite
        else :
            row['favorite'] = False

        randoms.append(row)

    context = get_context(request)
    context['mostviews'] = mostviews
    context['randoms'] = randoms

    return render(request,"index.html",context)
