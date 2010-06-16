
var lat=48.2;
var lon=16.35;
var zoom=12;

var map;

function init_map() {
	
    map = new OpenLayers.Map ("map", {
        controls:[
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.PanZoomBar(),
            new OpenLayers.Control.ScaleLine(),
            new OpenLayers.Control.MousePosition(),
            new OpenLayers.Control.Attribution()],
        maxExtent: new OpenLayers.Bounds(-20037508.34,-20037508.34,20037508.34,20037508.34),
                    maxResolution: 156543.0399,
        numZoomLevels: 19,
        units: 'm',
        projection: new OpenLayers.Projection("EPSG:900913"),
        displayProjection: new OpenLayers.Projection("EPSG:4326")
    } );

    layer_osm = new OpenLayers.Layer.OSM.Mapnik("OpenStreetMap");
    layer_osm.attribution = 'Map ' + layer_osm.attribution;
    map.addLayer(layer_osm);
    
    var style = new OpenLayers.Style({
        externalGraphic: '${icon}',
        graphicWidth: '${width}',
        graphicHeight: '${height}',
        graphicXOffset: -13,
        graphicYOffset: -29,
        graphicTitle: '${title}',
        graphicZIndex: 0,
        cursor: 'pointer',
        graphicOpacity:0.8
    },{
        context: {
            title: function(feature) {
                return (feature.cluster) ? feature.cluster.length + ' resources' : feature.data.title;
            },
            icon: function(feature) {
            	return MEDIA_URL + 'images/' + (feature.cluster ? 'flowers.png' : 'flower.png');
            },
            width: function(feature) {
                return (feature.cluster) ? 30 : 26;
            },
            height: function(feature) {
                return (feature.cluster) ? 35 : 30;
            }
        }
    });
    
    var select_style = OpenLayers.Util.extend({}, style);
    select_style.graphicOpacity = 1.0;
    select_style.graphicZIndex = 1;

    // http://openflights.org/blog/2009/10/21/customized-openlayers-cluster-strategies/
    var strategy = new OpenLayers.Strategy.Cluster({distance: 8, threshold: 2});
    var strategy2 = new OpenLayers.Strategy.Cluster({distance: 30, threshold: 8});
    
    layer_vector = new OpenLayers.Layer.Vector("Vectors", {
        attribution: 'Resource Data CC-By-NC-SA by <a href="http://vivirbien.mediavirus.org/">Vivir Bien</a>',
        styleMap: new OpenLayers.StyleMap({
            "default": style,
            "select": select_style}),
        strategies: [strategy2, strategy],
        projection: new OpenLayers.Projection("EPSG:4326"),
        rendererOptions: {yOrdering: true}
    });
    
    map.addLayer(layer_vector);
    
    /*
    var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
    map.setCenter (lonLat, zoom);
*/

    var select = new OpenLayers.Control.SelectFeature(layer_vector, {
        onSelect: function(feature) {
            var content = "";
            if (feature.cluster) {
                content += "<h4>" + feature.cluster.length + " Resources</h4>"
                for (var i=0; i < feature.cluster.length; i++) {
                    content += "<a href='" + feature.cluster[i].data.url + "'>"+feature.cluster[i].data.title + "</a><br />";
                }
            }
            else {
                content = "<a href='" + feature.data.url + "'>"+feature.data.title + "</a>";
            }
            popup = new OpenLayers.Popup.FramedCloud("chicken", 
                                     feature.geometry.getBounds().getCenterLonLat(),
                                     new OpenLayers.Size(100,100),
                                     content,
                                     null, true, onPopupClose);
            feature.popup = popup;
            map.addPopup(popup);
        },
        onUnselect: function(feature) {
            if (feature.popup) {
                map.removePopup(feature.popup);
                feature.popup.destroy();
                delete feature.popup;
            }
        }
    });
    map.addControl(select);
    select.activate();

    function onPopupClose(evt) {
        select.unselectAll();
    }
}

function add_content(features, adjust_viewport) {
	bounds = new OpenLayers.Bounds();
    for (var i=0; i<features.length; i++) {
        bounds.extend(features[i].geometry);
    }
    layer_vector.addFeatures(features);
    if (adjust_viewport) {
        map.zoomToExtent(bounds);
	    if (features.length < 2) {
	    	// single feature would cause full zoom-in
            map.zoomTo(13);
	    }
    }
}

$(document).ready(function(){
    $.get('/resources/json/view/' + VIEW + '/',function(data) {

        $('.map-loading').hide();
        
	    var geojson_format = new OpenLayers.Format.GeoJSON({
	        internalProjection: new OpenLayers.Projection("EPSG:900913"),
	        externalProjection: new OpenLayers.Projection("EPSG:4326")
	    });
	    
	    var features = geojson_format.read(data);
	    
	    if (features.length > 0) {
            $('#map').show();
	    	init_map();
	    	add_content(features, true);
	    }
    });

});

/*
    var control = new OpenLayers.Control.EditingToolbar(layer_vector);
    map.addControl(control);
    control.activate();
        
    var control = new OpenLayers.Control.DrawFeature(layer_vector, OpenLayers.Handler.Point);
    map.addControl(control);
    control.activate();
*/   
      
/*    
    var proj = new OpenLayers.Projection("EPSG:4326");
    
    var point = new OpenLayers.Geometry.Point(lon,lat).transform(proj, map.getProjectionObject());
    var pointFeature = new OpenLayers.Feature.Vector(point, {title: 'Marker 1'});
    
    var point2 = new OpenLayers.Geometry.Point(lon+0.01,lat+0.01).transform(proj, map.getProjectionObject());
    var pointFeature2 = new OpenLayers.Feature.Vector(point2, {title: 'Marker 2'});
    
    layer_vector.addFeatures([pointFeature,pointFeature2]);
*/      
