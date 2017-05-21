/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define([
	"jquery.sap.global", "sap/ui/fl/FlexController", "sap/ui/fl/Utils"
], function(jQuery, FlexController, Utils) {
	"use strict";

	/**
	 * Factory to create new instances of {sap.ui.fl.FlexController}
	 * @constructor
	 * @alias sap.ui.fl.FlexControllerFactory
	 * @experimental Since 1.27.0
	 * @author SAP SE
	 * @version 1.46.7
	 */
	var FlexControllerFactory = {};

	FlexControllerFactory._instanceCache = {};

	/**
	 * Creates or returns an instance of the FlexController
	 *
	 * @public
	 * @param {String} sComponentName The name of the component
	 * @returns {sap.ui.fl.FlexController} instance
	 *
	 */
	FlexControllerFactory.create = function(sComponentName) {
		var oFlexController = FlexControllerFactory._instanceCache[sComponentName];

		if (!oFlexController){
			oFlexController = new FlexController(sComponentName);
			FlexControllerFactory._instanceCache[sComponentName] = oFlexController;
		}

		return oFlexController;
	};

	/**
	 * Creates or returns an instance of the FlexController for the specified control.
	 * The control needs to be embedded into a View and the view needs to be embedded into a component.
	 * If one of this prerequisites is not fulfilled, no instance of FlexController will be returned.
	 *
	 * @public
	 * @param {sap.ui.core.Control} oControl The control
	 * @returns {sap.ui.fl.FlexController} instance
	 */
	FlexControllerFactory.createForControl = function(oControl) {
		var sComponentName = Utils.getComponentClassName(oControl);
		return FlexControllerFactory.create(sComponentName);
	};

	return FlexControllerFactory;
}, true);
