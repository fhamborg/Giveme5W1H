/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides the Design Time Metadata for the sap.m.Text control
sap.ui.define([],
	function () {
		"use strict";

		return {
			actions: {
				remove: {
					changeType: "hideControl"
				},
				rename: {
					changeType: "rename",
					domRef: function (oControl) {
						return oControl.$()[0];
					}
				},
				reveal: {
					changeType: "unhideControl"
				}
			},
			name: {
				singular: "TEXT_NAME",
				plural: "TEXT_NAME_PLURAL"
			}
		};
	}, /* bExport= */ false);