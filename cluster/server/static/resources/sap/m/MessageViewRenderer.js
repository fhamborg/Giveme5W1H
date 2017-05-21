/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(function(){"use strict";var M={};var C="sapMMsgView";M.render=function(r,c){r.write("<div");r.writeControlData(c);r.writeStyles();r.addClass(C);r.writeClasses();r.write(">");r.renderControl(c._navContainer);r.write("</div>");};return M;},true);
