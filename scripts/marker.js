var map;

function initialize() {
  var latlng = new google.maps.LatLng(35.5553063, 139.7225792);
  var options = {
    zoom: 18,
    center: latlng,
    mapTypeId: google.maps.MapTypeId.ROADMAP
  };
  map = new google.maps.Map(document.getElementById("map_canvas"), options);
  map.setCenter(latlng);
}

function loadJson(){
  $(function(){
    $.getJSON("C:\\aaa\\data.json" , function(data) {
    var json = data;
    for (i = 0; i < json.length; i++) {
    latlng = new google.maps.LatLng(json[i].lat,  json[i].lng);
    var marker = new google.maps.Marker({
        position: latlng, 
        map: map,});
    }
    });
  });
}