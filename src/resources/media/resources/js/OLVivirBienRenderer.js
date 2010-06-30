/**
 * @requires OpenLayers/Renderer/SVG.js
 */

/**
 * Class: OpenLayers.Renderer.VivirBienRenderer
 * 
 * Inherits:
 *  - <OpenLayers.Renderer.SVG>
 */
OpenLayers.Renderer.VivirBienRenderer = OpenLayers.Class(OpenLayers.Renderer.SVG, {

    initialize: function(containerID) {
        OpenLayers.Renderer.SVG.prototype.initialize.apply(this,arguments);

        //alert("hello from vivirbien renderer!");
    },

    /** 
     * Parameters:
     * geometry - {<OpenLayers.Geometry>}
     * style - {Object}
     * 
     * Returns:
     * {String} The corresponding node type for the specified geometry
     */
    getNodeType: function(geometry, style) {
    	// create svg group element for complex markers
    	// this will be filled with content in setStyle
    	if (geometry.CLASS_NAME == "OpenLayers.Geometry.Point" &&
    	    style.icon) {
    		return "g";
    	}
    	else {
    		return OpenLayers.Renderer.SVG.prototype.getNodeType(geometry, style);
    	}
    },

    /** 
     * Method: setStyle
     * Use to set all the style attributes to a SVG node.
     *
     * Parameters:
     * node - {SVGDomElement} An SVG element to decorate
     * style - {Object}
     * options - {Object} Currently supported options include 
     *                              'isFilled' {Boolean} and
     *                              'isStroked' {Boolean}
     */
    setStyle: function(node, style, options) {
        if (node._geometryClass == "OpenLayers.Geometry.Point" && style.icon) {
        	
        	// remove all children
        	while (node.firstChild) {
			     node.removeChild(node.firstChild);
			}
        	
            var icon = document.createElementNS(this.xmlns, "image");
            icon.setAttributeNS(null, "width", 20);
            icon.setAttributeNS(null, "height", 20);
            icon.setAttributeNS(null, "x", style.iconXOffset || 0);
            icon.setAttributeNS(null, "y", style.iconYOffset || 0);            
            icon.setAttributeNS(this.xlinkns, "href", style.iconBaseURL + style.icon);
            node.appendChild(icon);

            if (style.mask) {
	            var mask = document.createElementNS(this.xmlns, "image");
	            mask.setAttributeNS(null, "width", 26);
	            mask.setAttributeNS(null, "height", 28);
	            mask.setAttributeNS(this.xlinkns, "href", style.iconBaseURL + style.mask);
	            node.appendChild(mask);
            }
            
            if (style.subicons) {
                if (typeof style.subicons == "string") {
                    style.subicons = style.subicons.split('|');
                }
                if (style.subicontitles && typeof style.subicontitles == "string") {
                    style.subicontitles = style.subicontitles.split('|');
                }
            	for (var i=0; i<style.subicons.length; i++) {
            		var img = style.subicons[i];
            		// ignore empty strings
            		if (img.length == 0) continue;
            		
            		var sicon = document.createElementNS(this.xmlns, "image");
		            sicon.setAttributeNS(null, "width", 8);
		            sicon.setAttributeNS(null, "height", 8);
		            sicon.setAttributeNS(null, "x", 20 + (i - i%3) / 3 * 10);
		            sicon.setAttributeNS(null, "y", -1 + i%3 * 10);            
		            sicon.setAttributeNS(this.xlinkns, "href", style.iconBaseURL + img);
                    if (style.subicontitles && style.subicontitles[i]) {
                        sicon.setAttributeNS(null, "title", style.subicontitles[i]);    
                    }
		            node.appendChild(sicon);
		            if (style.subiconmask) {
		                var smask = document.createElementNS(this.xmlns, "image");
		                smask.setAttributeNS(null, "width", 10);
		                smask.setAttributeNS(null, "height", 10);
	                    smask.setAttributeNS(null, "x", 19 + (i - i%3) / 3 * 10);
	                    smask.setAttributeNS(null, "y", -2 + i%3 * 10);            
		                smask.setAttributeNS(this.xlinkns, "href", style.iconBaseURL + style.subiconmask);
	                    if (style.subicontitles && style.subicontitles[i]) {
	                        smask.setAttributeNS(null, "title", style.subicontitles[i]);    
	                    }
		                node.appendChild(smask);	            	
		            }
            	}
            }
            
            
            if (style.graphicTitle) {
                node.setAttributeNS(null, "title", style.graphicTitle);
            }
            var xOffset = (style.graphicXOffset != undefined) ?
                style.graphicXOffset : -(0.5 * width);
            var yOffset = (style.graphicYOffset != undefined) ?
                style.graphicYOffset : -(0.5 * height);

            var opacity = style.graphicOpacity || style.fillOpacity;
            node.setAttributeNS(null, "style", "opacity: "+opacity);
            
            pos = this.getPosition(node);
            node.setAttributeNS(null, "transform", "translate(" + (pos.x + xOffset).toFixed() + "," + (pos.y + yOffset).toFixed() + ")");

	        if (style.pointerEvents) {
	            node.setAttributeNS(null, "pointer-events", style.pointerEvents);
	        }
	                
	        if (style.cursor != null) {
	            node.setAttributeNS(null, "cursor", style.cursor);
	        }
            
            return node;        	
        }
        else {
        	return OpenLayers.Renderer.SVG.prototype.setStyle(node, style, options);
        }
    },
    
    /**
     * Method: getFeatureIdFromEvent
     * 
     * Parameters:
     * evt - {Object} An <OpenLayers.Event> object
     *
     * Returns:
     * {<OpenLayers.Geometry>} A geometry from an event that 
     *     happened on a layer.
     */
    getFeatureIdFromEvent: function(evt) {
    	// search up the tree for complex markers
        var target = evt.target;
        while (target && !target._featureId) {
            target = target.parentNode;
        }

        if (target && target._featureId) {
            return target._featureId;
        }
        
        return null;
    },

    CLASS_NAME: "OpenLayers.Renderer.VivirBienRenderer"
});

