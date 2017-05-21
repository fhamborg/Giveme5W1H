/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/table/Row'],function(q,R){"use strict";var a={};a.render=function(r,A){r.write("<div");r.writeControlData(A);r.addClass("sapUiTableAction");if(!(A.getParent()instanceof R)||!A._show){r.addStyle("display","none");}if(!A.getVisible()){r.addClass("sapUiTableActionHidden");}r.writeClasses();r.writeStyles();var t=A.getTooltip_AsString();if(t){r.writeAttributeEscaped("title",t);}r.write(">");var i=A.getAggregation("_icons");r.write("<div>");r.renderControl(i[0]);r.write("</div>");r.write("<div>");r.renderControl(i[1]);r.write("</div>");r.write("</div>");};return a;},true);
