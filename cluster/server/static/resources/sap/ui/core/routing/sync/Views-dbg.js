/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'], function(jQuery) {
	"use strict";

	/**
	 * Provide methods for sap.ui.core.routing.Views in sync mode
	 * @private
	 * @experimental
	 * @since 1.33
	 */
	return {

		/**
		 * @private
		 */
		_getViewWithGlobalId : function (oOptions) {
			function fnCreateView() {
				return sap.ui.view(oOptions);
			}

			if (!oOptions) {
				jQuery.sap.log.error("the oOptions parameter of getView is mandatory", this);
			}

			var oView,
				sViewName = oOptions.viewName;

			this._checkViewName(sViewName);
			oView = this._oViews[sViewName];

			if (oView) {
				return oView;
			}

			if (this._oComponent) {
				oView = this._oComponent.runAsOwner(fnCreateView);
			} else {
				oView = fnCreateView();
			}

			this._oViews[sViewName] = oView;

			this.fireCreated({
				view: oView,
				viewOptions: oOptions
			});

			return oView;
		}
	};
});
