/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/m/Breadcrumbs","sap/m/Text"],function(C,T){"use strict";var B={};B.render=function(r,c){var a=c._getControlsForBreadcrumbTrail(),s=c._getSelect();r.write("<ul");r.writeControlData(c);r.addClass("sapMBreadcrumbs");r.writeClasses();r.writeAttribute("role","navigation");r.writeAttributeEscaped("aria-label",C._getResourceBundle().getText("BREADCRUMB_LABEL"));r.write(">");if(s.getVisible()){this._renderControlInListItem(r,s,false,"sapMBreadcrumbsSelectItem");}a.forEach(function(o){this._renderControlInListItem(r,o,o instanceof T);},this);r.write("</ul>");};B._renderControlInListItem=function(r,c,s,a){r.write("<li");r.writeAttribute("role","presentation");r.writeAttribute("aria-hidden","true");r.addClass("sapMBreadcrumbsItem");r.addClass(a);r.writeClasses();r.write(">");r.renderControl(c);if(!s){r.write("<span");r.addClass("sapMBreadcrumbsSeparator");r.writeClasses();r.write(">/</span>");}r.write("</li>");};return B;},true);
