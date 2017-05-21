/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides object sap.ui.fl.Processor
sap.ui.define([
	'jquery.sap.global', 'sap/ui/base/Object'
], function(jQuery, BaseObject) {
	'use strict';

	/**
	 * The implementation of the <code>Preprocessor</code> for the SAPUI5 flexibility services that can be hooked in the <code>View</code> life cycle.
	 *
	 * @name sap.ui.fl.Preprocessor
	 * @class
	 * @constructor
	 * @author SAP SE
	 * @version 1.46.7
	 * @experimental Since 1.27.0
	 * @implements sap.ui.core.mvc.View.Preprocessor
	 */
	return BaseObject.extend("sap.ui.fl.Preprocessor", {});

}, /* bExport= */true);
