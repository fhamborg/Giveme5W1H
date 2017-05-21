/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";var N={};N.render=function(r,c){var s=c.getSubheader();var t=c.getTooltip_AsString();if(typeof t!=="string"){t="";}r.write("<div");r.writeControlData(c);r.writeAttribute("id",c.getId()+"-news-content");r.writeAttribute("role","presentation");r.writeAttributeEscaped("aria-label",t);r.addClass("sapMNwC");if(c.hasListeners("press")){r.addClass("sapMPointer");r.writeAttribute("tabindex","0");}r.writeClasses();r.write(">");r.write("<div");r.addClass("sapMNwCCTxt");r.writeClasses();r.write(">");r.renderControl(c._oContentText);r.write("</div>");r.write("<div");r.writeAttribute("id",c.getId()+"-subheader");r.addClass("sapMNwCSbh");r.writeClasses();r.write(">");r.writeEscaped(s);r.write("</div>");r.write("</div>");};return N;},true);
