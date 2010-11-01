var Theme = new Object();
Theme.color = 'blacks';

var Player = new Object();
var ols = new Array();

Player.onInit = function() {
    this.position = 0;
    this.nowPlaying = 0;
    this._p = document.getElementById("pos");
    this.flash = document.getElementById("myFlash");
    this.uri = '';
    
    this.pl = '#main';
    
    this.songs = new Array();
    
    this.load();
};

Player.onUpdate = function() {
    var isPlaying = (this.isPlaying == "true");
    //this.position;
    //this.duration;
    //this.bytesPercent;
    
    //progressSlider.setValue(_percent);
    if (this.bytesPercent == 100) {
        var onePercent = this.duration/100;
        if (this.position/onePercent > 99) {
            this.playNext();
        }
    }
    
    /*
    this._p = document.getElementById("pos");
    this._b = document.getElementById("bits");
    var _percent = this.position / (this.duration / 100);
    this._p.innerHTML = this.position + '/' + this.duration + '|' + _percent;
    this._b.innerHTML = this.bytesLoaded + "/" + this.bytesTotal + " ("     + this.bytesPercent + "%)";

    
    // Filled bar {
    if (undefined != document.getElementById('filled')) {
        var filled = document.getElementById('filled');
        filled.style.width = 7.5 * parseInt(_percent);
    }
    // }
    
    // Download Filled bar {
    if (undefined != document.getElementById('downloadFilled')) {
        var dfilled = document.getElementById('downloadFilled');
        dfilled.style.width = 7.5 * parseInt(this.bytesPercent);
    }
    // }*/
    
    /*if (this.isPlaying) {
        document.getElementById('nowName').innerHTML = this._formatName(this.songs[this.nowPlaying]);
        document.getElementById('downloadIt').style.display = 'inline';
        document.getElementById('downloadIt').href = this.songs[this.nowPlaying].uri;
    }*/
    
    // IDv3 {
    if (this.isPlaying == 'true') {
        dojo.byId('now_playing_uri').value = window.location.href.replace(window.location.hash, '') + this.pl + '/play/' + this.nowPlaying;
        
        window.location.hash = this.pl + '/play/' + this.nowPlaying;
        /*console.log(this.id3_artist);
        console.log(this.id3_album);
        console.log(this.id3_songname);
        console.log(this.id3_genre);
        console.log(this.id3_year);
        console.log(this.id3_track);
        console.log(this.id3_comment);*/

    } else {
      window.location.hash = this.pl;
    }
    //}

}
Player.play = function(id) {
    var _uri = 'http://www.ex.ua/get/450580';
    
    if (id == -1) {
      id = this.nowPlaying;
    }
    
    if (this.uri != '' && id == undefined) {
        id = this.nowPlaying;
    } else {
        if (undefined == this.songs[id]) {
            id = 0;
        }
        _uri = this.songs[id].uri;
        
        this.flash.SetVariable("method:setUrl", _uri);
        this.uri = _uri;
        this.nowPlaying = id;
    }
    
    
    this.flash.SetVariable("method:play", "");
    this.flash.SetVariable("enabled", "true");
    
    // Setting Volume
    /*if (undefined != volumeSlider) {
        this.setVolume(volumeSlider.value);
    }*/
    
    for (var d in ols) {
        dojo.removeClass(ols[d],'bold');
    }
    
    dojo.addClass(ols[id],'bold');
}

Player.pause = function() {
    this.flash.SetVariable("method:pause", "");
}

Player.stop = function() {
    this.flash.SetVariable("method:stop", "");
}

Player.load_list = function(type, play, id) {
  window.location.hash = '#' + type;

  if (play) {
    window.location.hash += '/play';
    if (id) {
      window.location.hash += '/' + parseInt(id);
    }
  }
  Player.load();
}

Player.load = function() {
    var uri = '/main.json';
    var auto_play = false;
    if (undefined != mainJsonUri) {
        uri = mainJsonUri;
    }
    if (window.location.hash == '#my') {
        uri = '/api/playlist/my.json';
        this.pl = '#my';
    }
    
    if (window.location.hash.substr(0, 5) == '#main') {
      var _play = window.location.hash.split('/');
      if (_play[0] == '#main') {
        this.pl = '#main';
        uri = '/api/songs/main.json';
      }
      if ((_play.length >= 2) && (_play[1] == 'play')) {
        auto_play = true;
      }
      if (_play.length >= 3) {
        Player.nowPlaying = parseInt(_play[2]);
      }
    }
    
    if (window.location.hash.substr(0, 8) == '#artist/') {
      var _artist = window.location.hash.substr(8, window.location.hash.length).split('/');
      this.pl = '#artist';
      if (_artist.length >= 1) {
        this.pl += '/' + _artist[0];
        
        uri = '/api/songs/artist/' + _artist[0] + '.json';
        if ((_artist.length >= 2) && (_artist[1] == 'play')) {
          auto_play = true;
        }
        if (_artist.length >= 3) {
          Player.nowPlaying = parseInt(_artist[2]);
        } 
      }
    }
    
    if (window.location.hash.substr(0, 5) == '#play') {
      var _play = window.location.hash.split('/');
      if (_play[0] == '#play') {
        auto_play = true;
      }
      if (_play.length >= 2) {
        Player.nowPlaying = parseInt(_play[1]);
      }
    }
    
    dojo.xhrGet({
        url:uri,
        //url:"/api/songs/main.json",
        handleAs:"json",
        load: function(data){
            console.log('Loading complete');
            var list = dojo.byId('playlist');
            list.innerHTML = '';
            for(var i in data['songs']){
               ols[i] = document.createElement('li');
               ols[i].ids = i;
               ols[i].onclick = function() {
                   Player.play(this.ids);
               };
               ols[i].innerHTML = Player._formatName(data['songs'][i]);
               
               list.appendChild(ols[i]);
            }
            Player.songs = data['songs'];
            
            var loading = dojo.byId('loading');
            loading.style.display = 'none';
            var loadingShadow = dojo.byId('loading_shadow');
            loadingShadow.style.display = 'none';
            if (auto_play) {
              Player.play(-1);
            }
        }
    });
}

Player.setProgress = function(percent) {
    this.flash.SetVariable("method:setPosition", percent * (this.duration/100));
}

Player.setVolume = function(percent) {
    this.flash.SetVariable("method:setVolume", percent);
}

Player.playNext = function() {
    var nextId = (this.nowPlaying+1 == this.songs.length) ? 0 : parseInt(this.nowPlaying)+1;
    this.play(nextId);
}

Player.playPrev = function() {
    var prevId = (this.nowPlaying == 0) ? this.songs.length-1 : parseInt(this.nowPlaying)-1;
    this.play(prevId);
}

/*** ****/
Player._formatName = function(song, includeDownload) {
    var temp = '';
    
    temp += song.authorName + ' :: ';
    temp += song.name;
    temp += ' (' + song.albumName + ')';
    
    /*if (undefined != includeDownload) {
        temp += '<a href="' + song.uri + '" target="_blank">';
        temp += '<img src="/static/images/icons/';
            temp += Theme.color
            temp += '/16x16/download.png" alt="Download this song" align="left" />';
        temp += '</a>'
    }
    
    
    if (isUser && window.location.hash != '#my') {
        temp += '<a href="javascript:void(0);" onclick="Player.addToMy(\'' + song.uri + '\');">'
        temp += '<img src="/static/images/icons/building_go.png" /></a>';
    }*/
    
    return temp;
}

Player.addToMy = function(ura) {
    dojo.xhrGet({
        url:"/api/playlist/addToMy.json",
        content: {uri:ura},
        handleAs:"text",
        load: function(data){
            console.log('Loading complete');
            console.log(data);
        }
    });
}
