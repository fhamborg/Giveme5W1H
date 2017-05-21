/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'],function(q){"use strict";var F={};F.render=function(r,c){r.write("<div");r.writeControlData(c);r.addClass("sapMFT");r.writeClasses();if(c.getTooltip_AsString()){r.writeAttributeEscaped("title",c.getTooltip_AsString());}r.addStyle("width",c.getWidth()||null);r.addStyle("height",c.getHeight()||null);r.writeStyles();r.write(">");r.write(c._getDisplayHtml());r.write("</div>");};return F;},true);
