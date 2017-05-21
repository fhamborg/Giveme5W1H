/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides enumeration sap.ui.model.UpdateMethod
sap.ui.define(function() {
	"use strict";


	/**
	 * Different methods for update operations.
	 *
	 * @enum {string}
	 * @public
	 * @alias sap.ui.model.odata.UpdateMethod
	 */
	var UpdateMethod = {
		/**
		 * Update requests will be send with HTTP method <code>MERGE</code>.
		 *
		 * @public
		 */
		Merge: "MERGE",

		/**
		 * Update requests will be send with HTTP method <code>PUT</code>.
		 * @public
		 */
		Put: "PUT"
	};

	return UpdateMethod;

}, /* bExport= */ true);
