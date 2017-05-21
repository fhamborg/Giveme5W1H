/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";var I={};I.render=function(r,c){r.write("<div");r.writeControlData(c);r.addClass("sapMImageContent");var t=c.getTooltip_AsString();if(t){r.writeAttributeEscaped("title",t);}if(c.hasListeners("press")){r.addClass("sapMPointer");r.writeAttribute("tabindex","0");}r.writeClasses();r.write(">");var C=c.getAggregation("_content");if(C){C.addStyleClass("sapMImageContentImageIcon");r.renderControl(C);}r.write("</div>");};return I;},true);
