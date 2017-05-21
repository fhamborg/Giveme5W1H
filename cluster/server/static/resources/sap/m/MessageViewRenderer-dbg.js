/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define(function () {
	"use strict";

	var MessageViewRenderer = {};

	var CSS_CLASS = "sapMMsgView";

	MessageViewRenderer.render = function (oRm, oControl) {
		oRm.write("<div");
		oRm.writeControlData(oControl);
		oRm.writeStyles();
		oRm.addClass(CSS_CLASS);
		oRm.writeClasses();
		oRm.write(">");
		oRm.renderControl(oControl._navContainer);
		oRm.write("</div>");
	};

	return MessageViewRenderer;

}, /* bExport= */ true);
