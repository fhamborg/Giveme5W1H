/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/base/Object','sap/ui/core/service/Service'],function(q,B,S){"use strict";var a=B.extend("sap.ui.core.service.ServiceFactory",{metadata:{"library":"sap.ui.core"},constructor:function(s){B.apply(this);var f=typeof s==="object"?S.create(s):s;this._fnService=f;}});a.prototype.destroy=function(){B.prototype.destroy.apply(this,arguments);delete this._fnService;};a.prototype.createInstance=function(s){if(typeof this._fnService==="function"){return Promise.resolve(new this._fnService(s));}else{return Promise.reject(new Error("Usage of sap.ui.core.service.ServiceFactory requires a service constructor function to create a new service instance or to override the createInstance function!"));}};return a;});
