/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(function(){"use strict";var B={};B.render=function(r,c){if(!c.getVisible()){return;}r.write("<div");r.writeControlData(c);if(c._getSelectedViewContent()){r.addClass('sapUxAPBlockBase');r.addClass("sapUxAPBlockBase"+c.getMode());}else{var C=c.getMetadata().getName().split(".").pop();r.addClass('sapUxAPBlockBaseDefaultSize');r.addClass('sapUxAPBlockBaseDefaultSize'+C+c.getMode());}r.writeClasses();r.write(">");if(c._getSelectedViewContent()){r.renderControl(c._getSelectedViewContent());}r.write("</div>");};return B;},true);
