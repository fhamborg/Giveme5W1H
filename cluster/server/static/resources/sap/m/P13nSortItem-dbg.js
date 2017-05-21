/*
 * ! UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides control sap.m.P13nSortItem.
sap.ui.define([
	'jquery.sap.global', './library', 'sap/ui/core/Item'
], function(jQuery, library, Item) {
	"use strict";

	/**
	 * Constructor for a new P13nSortItem.
	 *
	 * @param {string} [sId] ID for the new control, generated automatically if no ID is given
	 * @param {object} [mSettings] initial settings for the new control
	 * @class Type for <code>sortItems</code> aggregation in P13nSortPanel control.
	 * @extends sap.ui.core.Item
	 * @version 1.46.7
	 * @constructor
	 * @public
	 * @since 1.26.0
	 * @alias sap.m.P13nSortItem
	 * @ui5-metamodel This control/element also will be described in the UI5 (legacy) designtime metamodel
	 */
	var P13nSortItem = Item.extend("sap.m.P13nSortItem", /** @lends sap.m.P13nSortItem.prototype */
	{
		metadata: {

			library: "sap.m",
			properties: {

				/**
				 * sap.m.P13nConditionOperation
				 */
				operation: {
					type: "string",
					group: "Misc",
					defaultValue: null
				},

				/**
				 * key of the column
				 */
				columnKey: {
					type: "string",
					group: "Misc",
					defaultValue: null
				}
			}
		}
	});

	P13nSortItem.prototype.setColumnKey = function(v) {
		return this.setProperty("columnKey", v, true);
	};

	P13nSortItem.prototype.setOperation = function(v) {
		return this.setProperty("operation", v, true);
	};

	return P13nSortItem;

}, /* bExport= */true);
