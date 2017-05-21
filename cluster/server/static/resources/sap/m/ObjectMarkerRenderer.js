/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/Renderer'],function(q,R){"use strict";var O={};O.render=function(r,c){r.write("<span ");r.writeControlData(c);r.addClass("sapMObjectMarker");if(c._isIconVisible()){r.addClass("sapMObjectMarkerIcon");}if(c._isTextVisible()){r.addClass("sapMObjectMarkerText");}r.writeClasses();r.write(">");r.renderControl(c._getInnerControl());r.write("</span>");};return O;},true);
