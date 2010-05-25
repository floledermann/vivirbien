
var lat=48.2;
var lon=16.35;
var zoom=12;

var map;

$(document).ready(function(){
	
	var media_url = MEDIA_URL || "";
	
    map = new OpenLayers.Map ("map", {
        controls:[
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.PanZoomBar(),
            new OpenLayers.Control.ScaleLine(),
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

    layer_osm = new OpenLayers.Layer.OSM.Mapnik("OpenStreetMap");
    layer_osm.attribution = 'Map ' + layer_osm.attribution;
    map.addLayer(layer_osm);
    
    // http://openflights.org/blog/2009/10/21/customized-openlayers-cluster-strategies/
    //var strategy = new OpenLayers.Strategy.Cluster({distance: 15, threshold: 3});
    
    /*
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
    */
    
    var lonLat = new OpenLayers.LonLat(lon, lat).transform(new OpenLayers.Projection("EPSG:4326"), map.getProjectionObject());
    map.setCenter (lonLat, zoom);

    var style = new OpenLayers.Style({
        externalGraphic: media_url + "images/flowers.png",
//        graphicWidth: 21,
//        graphicHeight: 25,
//        graphicXOffset: -10,
//        graphicYOffset: -25,
        graphicWidth: 32,
        graphicHeight: 37,
        graphicXOffset: -16,
        graphicYOffset: -35,
        graphicTitle: '${title}',
        cursor: 'pointer',
        graphicOpacity:0.8
    },{
        context: {
            title: function(feature) {
                return (feature.cluster) ? feature.cluster.length + ' resources' : feature.data.title;
            }
        }
    });
    
    var select_style = OpenLayers.Util.extend({}, style);
    select_style.graphicOpacity = 1.0;

    var strategy = new OpenLayers.Strategy.Cluster({distance: 8, threshold: 2});
    
    layer_vector = new OpenLayers.Layer.Vector("Vectors", {
        attribution: 'Resource Data CC-By-NC-SA by <a href="http://vivirbien.mediavirus.org/">Vivir Bien</a>',
        styleMap: new OpenLayers.StyleMap({
        	"default": style,
        	"select": select_style}),
        strategies: [strategy],
        projection: new OpenLayers.Projection("EPSG:4326")
    });
    
    map.addLayer(layer_vector);
    
    
    var proj = new OpenLayers.Projection("EPSG:4326");
    
    var point = new OpenLayers.Geometry.Point(lon,lat).transform(proj, map.getProjectionObject());
    var pointFeature = new OpenLayers.Feature.Vector(point, {title: 'Marker 1'});
    
    var point2 = new OpenLayers.Geometry.Point(lon+0.01,lat+0.01).transform(proj, map.getProjectionObject());
    var pointFeature2 = new OpenLayers.Feature.Vector(point2, {title: 'Marker 2'});
    
    //layer_vector.addFeatures([pointFeature,pointFeature2]);
    
    var geojson_format = new OpenLayers.Format.GeoJSON({
        internalProjection: new OpenLayers.Projection("EPSG:900913"),
        externalProjection: new OpenLayers.Projection("EPSG:4326")
    });
    
    $.get('/resources/json/',function(data) {
	    var features = geojson_format.read(data);
	    for (f in features) {
	    	f.data = {
	    	  //popupContentHTML: "Hello",
	    	  overflow: "hidden"	    	  
	    	}
/*	    	
	    	var markerClick = function (evt) {
                if (this.popup == null) {
                    this.popup = this.createPopup(true); // use closebox
                    map.addPopup(this.popup);
                    this.popup.show();
                } else {
                    this.popup.toggle();
                }
                //currentPopup = this.popup;
                OpenLayers.Event.stop(evt);
            };*/
	    	/*
	    	f.events.register("mousedown", feature, markerClick);
	    	*/
	    }
	    layer_vector.addFeatures(features);
    });

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
    
    //var control = new OpenLayers.Control.EditingToolbar(layer_vector);
    //map.addControl(control);
    //control.activate();
        
    //var control = new OpenLayers.Control.DrawFeature(layer_vector, OpenLayers.Handler.Point);
    //map.addControl(control);
    //control.activate();
    
    

});


