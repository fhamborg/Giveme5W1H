/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/Renderer'],function(q,R){"use strict";var N={};N.render=function(r,c){var g,a,b=c.getItems(),e=c.getExpanded();r.write("<ul");r.writeControlData(c);var w=c.getWidth();if(w&&e){r.addStyle("width",w);}r.writeStyles();r.addClass("sapTntNavLI");if(!e){r.addClass("sapTntNavLICollapsed");}r.writeClasses();a=e?'tree':'toolbar';r.writeAttribute("role",a);r.write(">");for(var i=0;i<b.length;i++){g=b[i];g.render(r,c);}r.write("</ul>");};return N;},true);
