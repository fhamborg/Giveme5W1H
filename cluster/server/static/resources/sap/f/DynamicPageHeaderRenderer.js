/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";var D={};D.render=function(r,d){var c=d.getContent(),h=c.length>0,p=sap.ui.Device.system.phone,H=d.getPinnable()&&h&&!p;r.write("<header");r.writeControlData(d);r.writeAccessibilityState({role:"region"});r.addClass("sapContrastPlus");r.addClass("sapFDynamicPageHeader");if(H){r.addClass("sapFDynamicPageHeaderPinnable");}if(h){r.addClass("sapFDynamicPageHeaderWithContent");}r.writeClasses();r.write(">");if(h){r.write("<div");r.addClass("sapFDynamicPageHeaderContent");r.writeClasses();r.write(">");c.forEach(r.renderControl);r.write("</div>");if(H){D._renderPinUnpinArea(d,r);}}r.write("</header>");};D._renderPinUnpinArea=function(d,r){r.write("<div");r.addClass("sapFDynamicPageHeaderPinButtonArea");r.writeClasses();r.write(">");r.renderControl(d._getPinButton());r.write("</div>");};return D;},true);
