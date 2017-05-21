/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/m/OverflowToolbarButton','sap/m/ButtonRenderer'],function(O,B){"use strict";var S=O.extend("sap.m.semantic.SemanticOverflowToolbarButton",{renderer:B.render});S.prototype._getTooltip=function(){var t=O.prototype._getTooltip.call(this);if(!t&&!this._bInOverflow&&this.getText()){t=this.getText();}return t;};return S;},false);
