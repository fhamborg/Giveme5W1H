/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides default renderer for control sap.m.Image
sap.ui.define(['jquery.sap.global', 'sap/ui/core/Renderer'],
	function(jQuery, Renderer) {
	'use strict';

	/**
	 * IconTabBarSelectList renderer.
	 * @author SAP SE
	 * @namespace
	 */
	var IconTabBarSelectListRenderer = {
	};


	/**
	 * Renders the HTML for the given control, using the provided {@link sap.ui.core.RenderManager}.
	 *
	 * @param {sap.ui.core.RenderManager} rm the RenderManager that can be used for writing to the Render-Output-Buffer
	 * @param {sap.ui.core.Control} control an object representation of the control that should be rendered
	 */
	IconTabBarSelectListRenderer.render = function(rm, control) {
		var i,
			item,
			items = control.getItems(),
			iconTabHeader = control._iconTabHeader,
			isTextOnly = true;

		if (iconTabHeader) {
			iconTabHeader._checkTextOnly(items);
			isTextOnly = iconTabHeader._bTextOnly;
			control._bIconOnly = control.checkIconOnly(items);
		}

		rm.write('<ul');
		rm.writeAttribute('role', 'listbox');
		rm.writeControlData(control);
		rm.addClass('sapMITBSelectList');

		if (isTextOnly) {
			rm.addClass('sapMITBSelectListTextOnly');
		}

		rm.writeClasses();

		rm.write('>');

		for (i = 0; i < items.length; i++) {
			item = items[i];
			item.renderInSelectList(rm, control);
		}

		rm.write('</ul>');
	};

	return IconTabBarSelectListRenderer;

}, /* bExport= */ true);
