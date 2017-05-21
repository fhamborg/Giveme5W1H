/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides default renderer for control sap.ui.table.ColumnMenu
sap.ui.define(['sap/ui/table/ColumnMenu'], function(Menu) {
	"use strict";
	// Renderer defined already in ColumnMenu.js -> Keep this file for legacy purposes (e.g. AMD module dependencies)
	return Menu.getMetadata().getRenderer();
}, /* bExport= */ true);
