/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define(["sap/m/SelectRenderer", "sap/ui/core/Renderer"
], function (SelectRenderer, Renderer) {
	"use strict";

	/**
	 * @class ObjectPageRenderer renderer.
	 * @static
	 */
	var HierarchicalSelectRenderer = Renderer.extend(SelectRenderer);

	HierarchicalSelectRenderer.addClass = function (oRm) {
		oRm.addClass("sapUxAPHierarchicalSelect");
	};

	return HierarchicalSelectRenderer;

}, /* bExport= */ true);
