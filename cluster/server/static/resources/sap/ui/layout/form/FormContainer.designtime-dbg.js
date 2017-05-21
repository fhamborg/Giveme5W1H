/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

// Provides the Design Time Metadata for the sap.ui.layout.form.FormContainer control
sap.ui.define([],
	function() {
	"use strict";

	function _allFormElementsInvisible(oFormContainer){

		return oFormContainer.getFormElements().every(function(oFormElement){
			return oFormElement.getVisible() === false;
		});
	}

	return {
		aggregations : {
			formElements : {
				domRef : function(oFormContainer) {
					var oDomRef = oFormContainer.getDomRef();
					if (!oDomRef && oFormContainer.getFormElements().length === 0 || _allFormElementsInvisible(oFormContainer)) {
						var oHeader = oFormContainer.getTitle() || oFormContainer.getToolbar();
						if (oHeader) {
							return oHeader.getDomRef();
						}
					} else {
						return oDomRef;
					}
				}
			}
		}
	};

}, /* bExport= */ false);