/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides the Design Time Metadata for the sap.ui.layout.HorizontalLayout control
sap.ui.define([],
	function() {
	"use strict";

	return {
		aggregations: {
			content: {
				domRef: ":sap-domref",
				actions: {
					move: "moveControls"
				}
			}
		},
		actions: {
			remove: {
				changeType: "hideControl"
			},
			reveal: {
				changeType: "unhideControl"
			}
		},
		name: {
			singular: "HORIZONTAL_LAYOUT_CONTROL_NAME",
			plural: "HORIZONTAL_LAYOUT_CONTROL_NAME_PLURAL"
		}
	};

}, /* bExport= */ false);
