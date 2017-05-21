/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define(["sap/ui/fl/RegistrationDelegator"
	],
	function(RegistrationDelegator) {
	"use strict";

	/**
	 * SAPUI5 library for UI Flexibility and Descriptor Changes and Descriptor Variants.
	 *
	 * @namespace
	 * @name sap.ui.fl
	 * @author SAP SE
	 * @version 1.46.7
	 * @private
	 * @sap-restricted
	 *
	 */

	sap.ui.getCore().initLibrary({
		name:"sap.ui.fl",
		version:"1.46.7",
		dependencies:["sap.ui.core","sap.m"],
		noLibraryCSS: true,
		extensions: {
			"sap.ui.support": {
				diagnosticPlugins: [
					"sap/ui/fl/support/Flexibility"
				]
			}
		}
	});

	RegistrationDelegator.registerAll();

	return sap.ui.fl;

}, /* bExport= */ true);
