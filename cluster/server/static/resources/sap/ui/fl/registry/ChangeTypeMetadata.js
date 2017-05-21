/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/fl/Utils","jquery.sap.global"],function(U,q){"use strict";var C=function(p){if(!p.name){U.log.error("sap.ui.fl.registry.ChangeType: Name required");}if(!p.changeHandler){U.log.error("sap.ui.fl.registry.ChangeType: ChangeHandler required");}this._name=p.name;this._changeHandler=p.changeHandler;if(p.labelKey){this._labelKey=p.labelKey;}if(p.tooltipKey){this._tooltipKey=p.tooltipKey;}if(p.iconKey){this._iconKey=p.iconKey;}if(p.sortIndex){this._sortIndex=p.sortIndex;}};C.prototype._name="";C.prototype._changeHandler="";C.prototype._sortIndex=0;C.prototype._labelKey="";C.prototype._tooltipKey="";C.prototype._iconKey="";C.prototype.getName=function(){return this._name;};C.prototype.getChangeHandler=function(){return this._changeHandler;};C.prototype.getLabel=function(){return this._labelKey;};C.prototype.getTooltip=function(){return this._tooltipKey;};C.prototype.getIcon=function(){return this._iconKey;};C.prototype.getSortIndex=function(){return this._sortIndex;};return C;},true);
