/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'],function(q){"use strict";var P={};P.render=function(r,p){var i=p.getId();var t=p.getTooltip_AsString();r.write("<div");r.writeControlData(p);r.addClass("sapMPlanCal");if(p._iSize!==undefined&&p._iSize!==null){r.addClass("sapMSize"+p._iSize);}if(!p.getSingleSelection()){r.addClass("sapMPlanCalMultiSel");}if(!p.getShowRowHeaders()){r.addClass("sapMPlanCalNoHead");}if(t){r.writeAttributeEscaped('title',t);}var w=p.getWidth();if(w){r.addStyle("width",w);}var h=p.getHeight();if(h){r.addStyle("height",h);}r.writeAccessibilityState(p);r.writeClasses();r.writeStyles();r.write(">");var T=p.getAggregation("table");r.renderControl(T);var a=p._oRB.getText("PLANNINGCALENDAR");r.write("<span id=\""+i+"-Descr\" class=\"sapUiInvisibleText\">"+a+"</span>");a=p._oRB.getText("PLANNINGCALENDAR_VIEW");r.write("<span id=\""+i+"-SelDescr\" class=\"sapUiInvisibleText\">"+a+"</span>");r.write("</div>");};return P;},true);
