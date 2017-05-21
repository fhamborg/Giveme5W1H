/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
// Provides the Design Time Metadata for the sap.m.Slider control
sap.ui.define([],
	function () {
		"use strict";

		return {
			actions: {
				remove: {
					changeType: "hideControl"
				},
				reveal: {
					changeType: "unhideControl"
				}
			},
			aggregations: {
				scale: {
					domRef: ":sap-domref > .sapMSliderTickmarks"
				}
			},
			name: {
				singular: "SLIDER_NAME",
				plural: "SLIDER_NAME_PLURAL"
			}
		};
	}, /* bExport= */ true);