<html>
<head>
 <title>Your music on pyDjama</title>
 <script type="text/javascript">
 var mainJsonUri = '/api/songs/main.json';
 </script>
</head>
<body>
<object 
    class="playerpreview" 
    id="myFlash" 
    type="application/x-shockwave-flash" 
    data="/static/player_mp3_js.swf" 
    width="1" 
    height="1">
    
    <param name="movie" value="/static/player_mp3_js.swf" />
    <param name="AllowScriptAccess" value="always" />
    <param name="FlashVars" value="listener=Player&amp;interval=500" />
    
</object>
{% if widgets.header %}
 {% for widget in widgets.header %}
  {{ widget }}
 {% endfor %}
{% endif %}

<div id="loading_shadow"></div>
<div id="loading">Loading</div>

<div id="player">
	<div class="controls">
        <ul>
            <li><a href="javascript:void(0);" onclick="Player.playPrev();">Prev</a></li>
            <li><a href="javascript:void(0);" onclick="Player.play();">Play</a></li>
            <li><a href="javascript:void(0);" onclick="Player.pause();">Pause</a></li>
            <li><a href="javascript:void(0);" onclick="Player.playNext();">Next</a></li>
            <li><a href="javascript:void(0);" onclick="Player.stop();">Stop</a></li>
        </ul>
    </div>
</div>
<ul id="playlist">
</ul>

<link rel="stylesheet" href="/static/css/alpha/index.css" type="text/css" />
<script src="http://ajax.googleapis.com/ajax/libs/dojo/1.5/dojo/dojo.xd.js" type="text/javascript"></script>
<script src="/static/js/player/player.js" type="text/javascript"></script>
{% if widgets.footer %}
 {% for widget in widgets.footer %}
  {{ widget }}
 {% endfor %}
{% endif %}
</body>
</html>