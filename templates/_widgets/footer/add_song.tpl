
<div id="add_song">
 <form action="/api/songs/add_song.json" method="post" id="add_song_form">
 <b>Add Song:</b><br />
 <label for="song_name">Song Name: </label><input type="text" id="song_name" name="song_name"><br />
 <label for="author_name">Author Name: </label><input type="text" id="author_name" name="author_name"><br />
 <label for="album_name">Album Name: </label><input type="text" id="album_name" name="album_name"><br />
 <label for="album_yeaar">Album Year: </label><input type="text" id="album_year" name="album_year"><br />
 <label for="song_uri">Song Uri: </label><input type="text" id="song_uri" name="song_uri"><br />
 <a href="javascript:void(0);" onclick="add_song('close');">Submit</a> | 
 <a href="javascript:void(0);" onclick="add_song('another');">Submit and add more</a> | 
 <a href="javascript:void(0);" onclick="add_song_close();">Cancel</a>
 </form>
</div>

<script type="text/javascript" src="/static/js/widgets/footer/add_song.js"></script>
<link rel="stylesheet" href="/static/css/widgets/footer/add_song.css" type="text/css" />
