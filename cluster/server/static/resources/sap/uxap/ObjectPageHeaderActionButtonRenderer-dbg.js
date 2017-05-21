/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define(["sap/m/ButtonRenderer", "sap/ui/core/Renderer"],
	function (ButtonRenderer, Renderer) {
		"use strict";

		/**
		 * @class ObjectPageRenderer renderer.
		 * @static
		 */
		var ObjectPageHeaderActionButtonRenderer = Renderer.extend(ButtonRenderer);


		return ObjectPageHeaderActionButtonRenderer;

	}, /* bExport= */ true);
