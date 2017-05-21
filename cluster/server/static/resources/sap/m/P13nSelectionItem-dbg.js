/*
 * ! UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides control sap.m.P13nSelectionItem.
sap.ui.define([
	'jquery.sap.global', './library', 'sap/ui/core/Item'
], function(jQuery, library, Item) {
	"use strict";

	/**
	 * Constructor for a new P13nSelectionItem.
	 *
	 * @param {string} [sId] ID for the new control, generated automatically if no ID is given
	 * @param {object} [mSettings] initial settings for the new control
	 * @class Type for <code>selectionItems</code> aggregation in <code>P13nSelectionPanel</code> control.
	 * @extends sap.ui.core.Item
	 * @version 1.46.7
	 * @constructor
	 * @author SAP SE
	 * @private
	 * @since 1.46.0
	 * @alias sap.m.P13nSelectionItem
	 * @ui5-metamodel This control/element also will be described in the UI5 (legacy) designtime metamodel
	 */
	var P13nSelectionItem = Item.extend("sap.m.P13nSelectionItem", /** @lends sap.m.P13nSelectionItem.prototype */
	{
		metadata: {

			library: "sap.m",
			properties: {

				/**
				 * Defines the unique table column key.
				 */
				columnKey: {
					type: "string",
					defaultValue: undefined
				},

				/**
				 * Defines the index of a table column.
				 */
				index: {
					type: "int",
					defaultValue: -1
				},

				/**
				 * Defines whether the <code>P13nSelectionItem</code> is selected.
				 */
				selected: {
					type: "boolean",
					defaultValue: false
				}
			}
		}
	});

	return P13nSelectionItem;

}, /* bExport= */true);
