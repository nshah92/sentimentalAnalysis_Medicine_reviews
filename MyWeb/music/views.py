from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render, get_object_or_404

from .models import Album

def index(request):
    all_albums = Album.objects.all()
    context = {'all_albums' : all_albums}
    return render(request, 'music/index.html', context)

def details(request, album_id):
    # try:
    #     album = Album.objects.get(pk=album_id)
    # except Album.DoesNotExist:
    #     raise Http404("Album does not exist!!")

    album = get_object_or_404(Album, pk=album_id)
    return render(request, 'music/detail.html', {'album' : album})


def favourite(request, album_id):
    album = get_object_or_404(Album, pk=album_id)
    try:
        select_song = album.song_set.get(pk=request.POST['song'])
        print select_song
    except (KeyError, Song.DoesNotExist):
        return render(request, 'music/detail.html', {
                'album': album,
                'error_message': "You did not select valid song",
        })
    else:
        select_song.is_favourite = True
        select_song.save()
        return render(request, 'music/detail.html', {'album': album})