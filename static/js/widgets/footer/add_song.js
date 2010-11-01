
function add_song(action) {
  var errors = false;
  dojo.forEach(['song_name', 'author_name', 'album_name', 'album_year', 'song_uri'], function(item){
    var _item = dojo.byId(item);
    
    _item.style.backgroundColor = '#F1FFDE';
    if (_item.value == '') {
      errors = true;
      _item.style.backgroundColor = '#FFDEDE';
    }
  });
    
  if (!errors) {
    dojo.xhrPost({
      form: dojo.byId("add_song_form"),
      handleAs: "json",
      load: function(data) {
        if (data.status == 1) {
          console.log(data.message);
          if (action == 'close') {
            add_song_close();
          } else {
            dojo.byId('song_name').value = '';
            dojo.byId('song_uri').value = '';
          }
        } else {
          alert(data.message);
        }
      },
      error: function(error) {
        console.log('error, crap!');
      }
    });
  }
}

function add_song_close() {
 var add_song_window = dojo.byId('add_song');
 add_song_window.style.display = 'none';
 Player.load();
}

function add_song_show() {
 var add_song_window = dojo.byId('add_song');
 add_song_window.style.display = 'block'; 
}
