/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define([
	'jquery.sap.global', './Base'
], function(jQuery, Base) {
	"use strict";

	/**
	 * Change handler for unhiding of a control.
	 * @alias sap.ui.fl.changeHandler.UnhideControl
	 * @author SAP SE
	 * @version 1.46.7
	 * @experimental Since 1.27.0
	 */
	var UnhideControl = { };

	/**
	 * Unhides a control.
	 *
	 * @param {sap.ui.fl.Change} oChange change object with instructions to be applied on the control map
	 * @param {sap.ui.core.Control} oControl control that matches the change selector for applying the change
	 * @param {object} mPropertyBag
	 * @param {object} mPropertyBag.modifier - modifier for the controls
	 * @public
	 */
	UnhideControl.applyChange = function(oChange, oControl, mPropertyBag) {
		mPropertyBag.modifier.setVisible(oControl, true);
		return true;
	};

	/**
	 * Completes the change by adding change handler specific content
	 *
	 * @param {sap.ui.fl.Change} oChange change object to be completed
	 * @param {object} oSpecificChangeInfo as an empty object since no additional attributes are required for this operation
	 * @public
	 */
	UnhideControl.completeChangeContent = function(oChange, oSpecificChangeInfo) {

		var oChangeJson = oChange.getDefinition();

		if (!oChangeJson.content) {
			oChangeJson.content = {};
		}

	};

	return UnhideControl;
},
/* bExport= */true);
