
var Theme = new Object();
Theme.color = 'blacks';

var startFrom = 0;

var Player = new Object();
var ols = new Array();

Player.onInit = function() {
    this.position = 0;
    this.nowPlaying = 0;
    this._p = document.getElementById("pos");
    this.flash = document.getElementById("myFlash");
    this.uri = '';
    
    this.songs = new Array();
    
    this.load();
};

Player.onUpdate = function() {
    var isPlaying = (this.isPlaying == "true");
    //this.position;
    //this.duration;
    //this.bytesPercent;
    
/*    
    this._p = document.getElementById("pos");
    this._b = document.getElementById("bits");
    this._p.innerHTML = this.position + '/' + this.duration + '|' + _percent;
    this._b.innerHTML = this.bytesLoaded + "/" + this.bytesTotal + " ("     + this.bytesPercent + "%)";
*/
    var _percent = this.position / (this.duration / 100);
    //progressSlider.setValue(_percent);
    if (this.bytesPercent == 100) {
        var onePercent = this.duration/100;
        if (this.position/onePercent > 99) {
            this.playNext();
        }
    }
    
    // Filled bar {
    if (undefined != document.getElementById('data')) {
        var filled = document.getElementById('data');
        filled.style.width = 5 * parseInt(_percent);
    }
    // }
    
    // Download Filled bar {
    if (undefined != document.getElementById('downloadFilled')) {
        var dfilled = document.getElementById('downloadFilled');
        dfilled.style.width = 5 * parseInt(this.bytesPercent);
    }
    // }

    // IDv3 {
    var pause = document.getElementById('bttnPause');
    if (this.isPlaying) {
        pause.src = '/static/images/icons/16/control_pause_blue.png';
    } else {
        pause.src = '/static/images/icons/16/control_pause.png';
    }
    //}

}
Player.play = function(id) {
    var _uri = 'http://www.ex.ua/get/450580';
    
    if (this.uri != '' && id == undefined) {
        console.log('Resume');
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
    if (undefined != volumeSlider) {
        this.setVolume(volumeSlider.value);
    }
    
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

Player.load = function(_uri) {
    var uri = '/main.json';
    if (undefined != mainJsonUri) {
        uri = mainJsonUri;
    }
    if (window.location.hash == '#my') {
        uri = '/api/playlist/my.json';
        
    }
    if ('undefined' != typeof(_uri)) {
        uri = _uri;
    }
    
    if (window.location.hash.substr(0,6) == '#play/') {
        var _income = window.location.hash.split('/');
        if (_income.length == 4) {
            uri = '/api/songs/' + _income[3] + '.json';
            startFrom = _income[1];
        } else {
            startFrom = _income[1];
        }
    }
    
    
    dojo.xhrGet({
        url:uri,
        //url:"/api/songs/main.json",
        handleAs:"json",
        load: function(data){
            console.log('Loading complete');
            var list = document.getElementById('list');
            list.innerHTML = '';
            var listTbody = document.createElement('tbody');
            list.appendChild(listTbody);
            var _pl = false;
            for(var i in data['songs']){
               var spl = data['songs'][i].uri.split('/');
               if (spl.length == 5 && startFrom != 0) {
                if (spl[4] == startFrom) {
                    _pl = i;
                }
               }
               ols[i] = document.createElement('tr');
               ols[i].ids = i;
               
               ols[i].tdId = document.createElement('td');
               ols[i].tdId.innerHTML = parseInt(i)+1;
               ols[i].tdId.ids = i;
               ols[i].tdId.onclick = function() {
                   Player.play(this.ids);
               };
               ols[i].appendChild(ols[i].tdId);
               
               ols[i].tdName = document.createElement('td');
               ols[i].tdName.innerHTML = data['songs'][i].name;
               ols[i].tdName.ids = i;
               ols[i].tdName.onclick = function() {
                   Player.play(this.ids);
               };
               ols[i].appendChild(ols[i].tdName);
               
               ols[i].tdAlbumName = document.createElement('td');
               ols[i].tdAlbumName.innerHTML = data['songs'][i].albumName;
               ols[i].tdAlbumName.ids = i;
               ols[i].tdAlbumName.onclick = function() {
                   Player.play(this.ids);
               };
               ols[i].appendChild(ols[i].tdAlbumName);
               
               ols[i].tdAuthorName = document.createElement('td');
               ols[i].tdAuthorName.innerHTML = data['songs'][i].authorName;
               ols[i].tdAuthorName.ids = i;
               ols[i].tdAuthorName.onclick = function() {
                   Player.play(this.ids);
               };
               ols[i].appendChild(ols[i].tdAuthorName);
               if (isUser) {
                   if (isMy) {
                       ols[i].tdBlock = document.createElement('td');
                       ols[i].tdBlock.innerHTML = "<a href='javascript:void(0);' onclick='Player.removeFromMy(\"" + data['songs'][i].uri + "\");'><img src='/static/images/icons/16/book_delete.png' alt='' /></a>";
                       ols[i].appendChild(ols[i].tdBlock);
                   } else {
                       ols[i].tdBlock = document.createElement('td');
                       ols[i].tdBlock.innerHTML = "<a href='javascript:void(0);' onclick='Player.addToMy(\"" + data['songs'][i].uri + "\");'><img src='/static/images/icons/16/book_go.png' alt='' /></a>";
                       ols[i].appendChild(ols[i].tdBlock);
                   }
               }
               listTbody.appendChild(ols[i]);
            }
            Player.songs = data['songs'];
            
            var loading = document.getElementById('loading');
            loading.style.display = 'none';
            var loadingShadow = document.getElementById('loadingShadow');
            loadingShadow.style.display = 'none';
            
            if (_pl) {
                Player.play(_pl);
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
    
    if (undefined != includeDownload) {
        temp += '<a href="' + song.uri + '" target="_blank">';
        temp += '<img src="/static/images/icons/';
            temp += Theme.color
            temp += '/16x16/download.png" alt="Download this song" align="left" />';
        temp += '</a>'
    }
    
    
    if (isUser && window.location.hash != '#my') {
        temp += '<a href="javascript:void(0);" onclick="Player.addToMy(\'' + song.key + '\');">'
        temp += '<img src="/static/images/icons/building_go.png" /></a>';
    }
    
    return temp;
}

Player.addToMy = function(ura) {
    
    var loading = document.getElementById('loading');
    loading.style.display = 'block';
    var loadingShadow = document.getElementById('loadingShadow');
    loadingShadow.style.display = 'block';

    dojo.xhrGet({
        url:"/api/playlist/add_to_my.json",
        content: {uri:ura},
        handleAs:"text",
        load: function(data){
            console.log('Loading complete');
            var loading = document.getElementById('loading');
            loading.style.display = 'none';
            var loadingShadow = document.getElementById('loadingShadow');
            loadingShadow.style.display = 'none';
        }
    });
}

Player.removeFromMy = function(ura) {
    
    var loading = document.getElementById('loading');
    loading.style.display = 'block';
    var loadingShadow = document.getElementById('loadingShadow');
    loadingShadow.style.display = 'block';

    dojo.xhrGet({
        url:"/api/playlist/remove_from_my.json",
        content: {uri:ura},
        handleAs:"text",
        load: function(data){
            console.log('Loading complete');
            var loading = document.getElementById('loading');
            loading.style.display = 'none';
            var loadingShadow = document.getElementById('loadingShadow');
            loadingShadow.style.display = 'none';
            Player.load('/api/playlist/my.json');
        }
    });
}


