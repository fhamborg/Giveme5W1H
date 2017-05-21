/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['./library'],function(l){"use strict";var B={};B.render=function(r,b){this.startLayout(r,b);this.addContent(r,b);this.endLayout(r);};B.startLayout=function(r,b){var a=b.getBackground();b.addStyleClass("sapUiBlockLayoutBackground"+a);r.write("<div");r.writeControlData(b);r.addClass("sapUiBlockLayout");r.writeStyles();r.writeClasses();r.write(">");};B.addContent=function(r,b){var c=b.getContent(),o=sap.ui.layout.BlockRowColorSets,t=Object.keys(o).map(function(k){return o[k];}),n=t.length;c.forEach(function(a,i,R){var T=a.getRowColorSet()||t[i%n],C="sapUiBlockLayoutBackground"+T,p=(i&&R[i-1])||null;if(p&&p.hasStyleClass(C)){a.removeStyleClass(C);C+="Inverted";}if(C){a.addStyleClass(C);}r.renderControl(a);});};B.endLayout=function(r){r.write("</div>");};return B;},true);
