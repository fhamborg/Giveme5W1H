/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/dt/ManagedObjectObserver'],function(q,M){"use strict";var C=M.extend("sap.ui.dt.ControlObserver",{metadata:{library:"sap.ui.dt",properties:{},associations:{"target":{"type":"sap.ui.core.Control"}},events:{"afterRendering":{}}}});C.prototype.init=function(){M.prototype.init.apply(this,arguments);this._oControlDelegate={onAfterRendering:this._onAfterRendering};};C.prototype.observe=function(c){M.prototype.observe.apply(this,arguments);c.addEventDelegate(this._oControlDelegate,this);};C.prototype.unobserve=function(){var c=this.getTargetInstance();if(c){c.removeDelegate(this._oControlDelegate,this);}M.prototype.unobserve.apply(this,arguments);};C.prototype._onAfterRendering=function(){this.fireAfterRendering();};return C;},true);
