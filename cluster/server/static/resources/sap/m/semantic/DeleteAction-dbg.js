/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define(['sap/m/semantic/SemanticButton'], function(SemanticButton) {
	"use strict";

	/**
	 * Constructor for a new DeleteAction.
	 * @param {string} [sId] ID for the new control, generated automatically if no ID is given
	 * @param {object} [mSettings] Custom initial settings for the new control
	 *
	 * @class
	 * A DeleteAction button has default semantic-specific properties and is
	 * eligible for aggregation content of a {@link sap.m.semantic.SemanticPage}.
	 *
	 * @extends sap.m.semantic.SemanticButton
	 *
	 * @author SAP SE
	 * @version 1.46.7
	 *
	 * @constructor
	 * @public
	 * @since 1.36
	 * @alias sap.m.semantic.DeleteAction
	 * @ui5-metamodel This control/element also will be described in the UI5 (legacy) designtime metamodel
	 */

	var DeleteAction = SemanticButton.extend("sap.m.semantic.DeleteAction", /** @lends sap.m.semantic.DeleteAction.prototype */ {
		metadata: {
			library: "sap.m"
		}
	});

	return DeleteAction;

}, /* bExport= */ true);
