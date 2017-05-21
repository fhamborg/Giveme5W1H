/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'],function(q){"use strict";var T={};T.render=function(r,c){var t=c._getTabStrip(),s=c._getSelectedItemContent();r.write("<div ");r.writeControlData(c);r.addClass("sapMTabContainer");r.addClass("sapContrastPlus");r.writeClasses();r.write(">");if(t){r.renderControl(t);}r.write("<div id='"+c.getId()+"-containerContent' ");r.addClass("sapMTabContainerContent");r.writeClasses();r.write(">");r.write("<div id='"+this.getContentDomId(c)+"' class='sapMTabContainerInnerContent'");r.writeAccessibilityState(c,this.getTabContentAccAttributes(c));r.write(">");if(s){s.forEach(function(C){r.renderControl(C);});}r.write("</div>");r.write("</div>");r.write("</div>");};T.getTabContentAccAttributes=function(c){var s=c.getSelectedItem(),t,a={role:"tabpanel"};if(s){t=c._toTabStripItem(s);if(t){a["aria-labelledby"]=t.getId();}}return a;};T.getContentDomId=function(c){return c.getId()+"-content";};return T;},true);
