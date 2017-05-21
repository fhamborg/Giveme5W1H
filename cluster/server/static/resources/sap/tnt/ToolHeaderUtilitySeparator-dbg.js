/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides control sap.tnt.ToolHeaderUtilitySeparator.
sap.ui.define(['jquery.sap.global', './library', 'sap/ui/core/Control'],
	function(jQuery, library, Control) {
		"use strict";


		/**
		 * Constructor for a new ToolHeaderUtilitySeparator.
		 *
		 * @param {string} [sId] ID for the new control, generated automatically if no ID is given
		 * @param {object} [mSettings] Initial settings for the new control
		 *
		 * @class
		 * The ToolHeaderUtilitySeparator control is used in the sap.tnt.ToolHeader control
		 * to specify where the overflow button is placed.
		 * @extends sap.ui.core.Control
		 *
		 * @author SAP SE
		 * @version 1.46.7
		 *
		 * @constructor
		 * @public
		 * @since 1.16
		 * @alias sap.tnt.ToolHeaderUtilitySeparator
		 * @ui5-metamodel This control/element also will be described in the UI5 (legacy) designtime metamodel
		 */
		var ToolHeaderUtilitySeparator = Control.extend("sap.tnt.ToolHeaderUtilitySeparator", /** @lends sap.tnt.ToolHeaderUtilitySeparator.prototype */ {
			metadata: {
				library: "sap.tnt",
				properties: {
				}
			},
			renderer: {
				render : function() {

				}
			}
		});

		return ToolHeaderUtilitySeparator;

	}, /* bExport= */ true);
