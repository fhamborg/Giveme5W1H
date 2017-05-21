/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/base/ManagedObject'],function(M){"use strict";var B=M.extend("sap.ui.fl.context.BaseContextProvider",{metadata:{properties:{text:{type:"String"},description:{type:"String"}}}});B.prototype.loadData=function(){return Promise.resolve({});};B.prototype.getValue=function(r){return this.loadData().then(function(d){var R=r&&r.split(".")||[];var m=R.reduce(function(c,C){if(c&&c.hasOwnProperty(C)){return c[C];}return undefined;},d);return m;});};B.prototype.getValueHelp=function(r){return Promise.resolve({});};B.prototype.validate=function(k,v){return Promise.resolve(true);};return B;},true);
