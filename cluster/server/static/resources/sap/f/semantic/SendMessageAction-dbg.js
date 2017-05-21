/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */

sap.ui.define(['sap/f/semantic/SemanticButton'], function(SemanticButton) {
	"use strict";

	/**
	* Constructor for a new <code>SendMessageAction</code>.
	* @param {string} [sId] ID for the new control, generated automatically if no ID is given
	* @param {object} [mSettings] Custom initial settings for the new control
	*
	* @class
	* A semantic-specific button, eligible for the <code>sendMessageAction</code> aggregation of the
	* {@link sap.f.semantic.SemanticPage} to be placed in the share menu within its title.
	*
	* @extends <code>sap.f.semantic.SemanticButton</code>
	*
	* @author SAP SE
	* @version 1.46.7
	*
	* @constructor
	* @public
	* @since 1.46.0
	* @alias sap.f.semantic.SendMessageAction
	* @ui5-metamodel This control/element also will be described in the UI5 (legacy) designtime metamodel
	*/
	var SendMessageAction = SemanticButton.extend("sap.f.semantic.SendMessageAction", /** @lends sap.f.semantic.SendMessageAction.prototype */ {
		metadata: {
			library: "sap.f"
		}
	});

	return SendMessageAction;
}, /* bExport= */ true);
