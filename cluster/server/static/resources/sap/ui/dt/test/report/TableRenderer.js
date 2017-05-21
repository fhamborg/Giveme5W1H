/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'],function(q){"use strict";var T={};T.render=function(r,t){r.addClass("sapUiDtTableReport");r.write("<div");r.writeControlData(t);r.writeStyles();r.writeClasses();r.write(">");r.renderControl(t._getTable());r.write("</div>");};return T;},true);
