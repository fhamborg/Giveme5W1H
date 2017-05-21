/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/fl/Utils","jquery.sap.global"],function(U,q){"use strict";var C=function(p){if(!p.changeTypeMetadata){U.log.error("sap.ui.fl.registry.ChangeRegistryItem: ChangeTypeMetadata required");}if(!p.controlType){U.log.error("sap.ui.fl.registry.ChangeRegistryItem: ControlType required");}this._changeTypeMetadata=p.changeTypeMetadata;this._controlType=p.controlType;if(p.permittedRoles){this._permittedRoles=p.permittedRoles;}if(p.dragTargets){this._dragTargets=p.dragTargets;}};C.prototype._changeTypeMetadata=undefined;C.prototype._controlType=undefined;C.prototype._permittedRoles={};C.prototype._dragTargets=[];C.prototype.getChangeTypeMetadata=function(){return this._changeTypeMetadata;};C.prototype.getChangeTypeName=function(){return this._changeTypeMetadata.getName();};C.prototype.getControlType=function(){return this._controlType;};C.prototype.getPermittedRoles=function(){return this._permittedRoles;};C.prototype.getDragTargets=function(){return this._dragTargets;};return C;},true);
