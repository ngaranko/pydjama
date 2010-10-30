
def format_json(songs):
    songs_json = ''
    id = 0
    for song in songs:
        songs_json += '{"key":"%s", "name":"%s", "author":1, "album":1, "uri":"%s",' % (song.key().id(), song.name, song.uri)
        if song.author:
            author = song.author
        else:
            author = 'VA'
        if song.album:
            album = song.album
        else:
            album = 'VA'
                
        songs_json = ''.join([songs_json,
                            '"authorName":"%s", "albumName":"%s"}' % (author, album)
                            ])
        
        id += 1
        if id != len(songs):
            songs_json += ','
    return songs_json
