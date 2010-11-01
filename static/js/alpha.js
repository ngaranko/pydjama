
dojo.addOnLoad(function(){
  dojo.byId('artists').innerHTML = '<li>Loading artists list..</li>';
  dojo.xhrGet({
        url:"/api/songs/main.json",
        handleAs:"json",
        load: function(data){
            console.log('Artists loading complete');
            var artists = new Array();
            var artists_html = '';
            
            dojo.forEach(data.songs, function(item) {
              if (artists[item.authorName] == undefined) {
                artists[item.authorName] = 1;
                artists_html += '<li onclick="' + format_artist_link(item.authorName) + '">' + item.authorName + '</li>';
              }
            });
            
            dojo.byId('artists').innerHTML = artists_html;
        }
    });
});

function format_artist_link(name) {
  name = name.replace(' ', '_');
  
  return "Player.load_list('artist/" + name + "');";
  
}
