/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides the Design Time Metadata for the sap.m.ObjectListItem control
sap.ui.define([],
	function() {
	"use strict";

	return {
		aggregations: {
			firstStatus: {
				domRef: ":sap-domref .sapMObjLStatus1DivEmpty"
			},
			secondStatus: {
				domRef: ":sap-domref .sapMObjLStatus2DivEmpty"
			},
			attributes: {
				domRef: ":sap-domref .sapMObjLAttrDivEmpty"
			}
		}
	};

}, /* bExport= */ false);
