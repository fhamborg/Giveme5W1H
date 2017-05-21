/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";return{display:function(){var v,n;this._oLastDisplayedTarget=null;var r=this._super.display.apply(this,arguments);if(this._oLastDisplayedTarget){v=this._getViewLevel(this._oLastDisplayedTarget);n=this._oLastDisplayedTarget._oOptions.name;}this._oTargetHandler.navigate({viewLevel:v,navigationIdentifier:n});return r;},_displaySingleTarget:function(n){var t=this.getTarget(n);if(t){this._oLastDisplayedTarget=t;}return this._super._displaySingleTarget.apply(this,arguments);}};},true);
