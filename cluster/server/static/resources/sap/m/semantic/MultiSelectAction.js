/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/m/semantic/SemanticToggleButton','sap/m/semantic/SemanticConfiguration'],function(S,a){"use strict";var M=S.extend("sap.m.semantic.MultiSelectAction",{metadata:{library:"sap.m"}});var b=sap.ui.getCore().getLibraryResourceBundle("sap.m");M._PRESSED_STATE_TO_ICON_MAP={"true":"sap-icon://sys-cancel","false":"sap-icon://multi-select"};M._ACC_TOOLTIP_TO_ICON_MAP={"true":b.getText("SEMANTIC_CONTROL_MULTI_SELECT_CANCEL"),"false":b.getText("SEMANTIC_CONTROL_MULTI_SELECT")};M.prototype._setPressed=function(p,s){var i=M._PRESSED_STATE_TO_ICON_MAP[p];var I=M._ACC_TOOLTIP_TO_ICON_MAP[p];this._getControl().setIcon(i);this._getControl().setTooltip(I);};return M;},true);
