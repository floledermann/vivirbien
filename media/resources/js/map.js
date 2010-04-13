
var lat=48.2;
var lon=16.35;
var zoom=12;

var map;

$(document).ready(function(){
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
        externalGraphic: "/media/images/marker.png",
        graphicWidth: 21,
        graphicHeight: 25,
        graphicXOffset: -10,
        graphicYOffset: -25,
        graphicTitle: '${title}'
    },{
        context: {
            title: function(feature) {
                return (feature.cluster) ? feature.cluster.length + ' resources' : feature.data.title;
            }
        }
    });

    var strategy = new OpenLayers.Strategy.Cluster({distance: 8, threshold: 2});
    
    layer_vector = new OpenLayers.Layer.Vector("Vectors", {
        attribution: 'Resource Data CC-By-NC-SA by <a href="http://vivirbien.mediavirus.org/">Vivir Bien</a>',
        styleMap: new OpenLayers.StyleMap({"default": style}),
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
    
    var featurecollection = {
              "type": "FeatureCollection", 
              "features": [
                {
                	"type": "Feature",
                	"id": "foobar-0",
                	"geometry": {
                            "type":"Point", 
                            "coordinates":[lon, lat]
                    },
                    "properties": {}
                }
              ]
           };
    var features = '{"resources": [{"type": "resource","location": "latlng:48.2,16.35"}]}';
    
    var geojson_format = new OpenLayers.Format.GeoJSON({
        internalProjection: new OpenLayers.Projection("EPSG:900913"),
        externalProjection: new OpenLayers.Projection("EPSG:4326")
    });
    
    var fts = geojson_format.read(features, null, function(key, value) {
        switch (key) {
        	case "resources":   break;
        }
        return value;
    });
    
    layer_vector.addFeatures(fts);

    //var control = new OpenLayers.Control.EditingToolbar(layer_vector);
    //map.addControl(control);
    //control.activate();
        
    //var control = new OpenLayers.Control.DrawFeature(layer_vector, OpenLayers.Handler.Point);
    //map.addControl(control);
    //control.activate();
    
    

});


