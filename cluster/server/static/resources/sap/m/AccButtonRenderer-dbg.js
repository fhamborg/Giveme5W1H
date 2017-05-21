/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define(['jquery.sap.global', './ButtonRenderer', 'sap/ui/core/Renderer'],
	function(jQuery, ButtonRenderer, Renderer) {
		"use strict";

	var AccButtonRenderer = Renderer.extend(ButtonRenderer);

	AccButtonRenderer.renderAccessibilityAttributes = function(oRm, oControl) {
		if (oControl.getTabIndex()) {
			oRm.writeAttribute("tabindex", oControl.getTabIndex());
		}
		if (oControl.getAriaHidden()){
			oRm.writeAttribute("aria-hidden", oControl.getAriaHidden());
		}
	};

	return AccButtonRenderer;
}, /* bExport= */ true);