/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";return{_place:function(p,d){var r=this._super._place.apply(this,arguments);this._oTargetHandler.addNavigation({navigationIdentifier:this._oOptions.name,transition:this._oOptions.transition,transitionParameters:this._oOptions.transitionParameters,eventData:d,targetControl:r.oTargetControl,view:r.oTargetParent,preservePageInSplitContainer:this._oOptions.preservePageInSplitContainer});if(d){delete d.routeConfig;}return r;}};},true);
