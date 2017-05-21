/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/fl/context/BaseContextProvider","sap/ui/Device"],function(B,D){"use strict";var a=B.extend("sap.ui.fl.context.DeviceContextProvider",{metadata:{properties:{text:{type:"String",defaultValue:"Device"},description:{type:"String",defaultValue:"Returns the values of sap.ui.Device"}}}});a.prototype.loadData=function(){return Promise.resolve(D);};a.prototype.getValueHelp=function(){return Promise.resolve({});};a.prototype.validate=function(k,v){return Promise.resolve(true);};return a;},true);
