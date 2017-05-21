/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define(['sap/ui/core/Renderer', './ListBaseRenderer'],
	function(Renderer, ListBaseRenderer) {
	"use strict";

	/**
	 * Tree renderer.
	 * @namespace
	 *
	 */
	var TreeRenderer = Renderer.extend(ListBaseRenderer);

	/**
	 * Returns the ARIA accessibility role.
	 *
	 * @param {sap.ui.core.Control} oControl An object representation of the control
	 * @returns {String}
	 */
	TreeRenderer.getAriaRole = function(oControl) {
		return "tree";
	};

	return TreeRenderer;

}, /* bExport= */ true);