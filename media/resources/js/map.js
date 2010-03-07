
var lat=48.2;
var lon=16.35;
var zoom=12;

var map;

$(document).ready(function(){
    map = new OpenLayers.Map ("map", {
        controls:[
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.PanZoomBar(),
            //new OpenLayers.Control.LayerSwitcher(),
            new OpenLayers.Control.MousePosition(),
            new OpenLayers.Control.Attribution()],
        maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
                    maxResolution: 156543.0399,
        numZoomLevels: 19,
        units: 'm',
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326")
    } );

    layerMapnik = new OpenLayers.Layer.OSM.Mapnik("OpenStreetMap");
    layerMapnik.attribution = 'Map ' + layerMapnik.attribution;
    map.addLayer(layerMapnik);
    layerMarkers = new OpenLayers.Layer.Markers("Resources");
    layerMarkers.attribution = 'Resource Data CC-By-NC-SA by <a href="http://vivirbien.mediavirus.org/">Vivir Bien</a>';
    
    // http://openflights.org/blog/2009/10/21/customized-openlayers-cluster-strategies/
    //var strategy = new OpenLayers.Strategy.Cluster({distance: 15, threshold: 3});
    
    var style = new OpenLayers.Style({
        externalGraphic: "${getIcon}",
        graphicWidth:"21",
        graphicHeight:"25",
        graphicOpacity:0.90,
        cursor:'pointer',
        strokeWidth: "${width}"
    } , {
        context: {
            width: function(feature) {
                return (feature.cluster) ? 2 : 1;
            }
        }
    }
    );
    
    //layerMarkers.strategies = [strategy];
    //layerMarkers.styleMap = new OpenLayers.StyleMap({"default": style});
     
    map.addLayer(layerMarkers);

    var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
    map.setCenter (lonLat, zoom);

    var size = new OpenLayers.Size(21,25);
    var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
    var icon = new OpenLayers.Icon('http://www.openstreetmap.org/openlayers/img/marker.png',size,offset);    
    var lonLat2 = new OpenLayers.LonLat(lon + 0.01, lat + 0.01).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());

    layerMarkers.addMarker(new OpenLayers.Marker(lonLat, icon));
    layerMarkers.addMarker(new OpenLayers.Marker(lonLat2, icon.clone()));


    /*
    var style_mark = OpenLayers.Util.extend({}, OpenLayers.Feature.Vector.style['default']);
    style_mark.graphicWidth = 24;
    style_mark.graphicHeight = 20;
    style_mark.graphicXOffset = -(style_mark.graphicWidth/2);  // this is the default value
    style_mark.graphicYOffset = -style_mark.graphicHeight;
    style_mark.externalGraphic = "marker.png";
    style_mark.graphicTitle = "this is a test tooltip";
   
    var point = new OpenLayers.Geometry.Point(lon, lat);
    
    var pointFeature = new OpenLayers.Feature.Vector(point, null, style_mark);
    layerMarkers.addFeatures([pointFeature]);
    */
    
});


