/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/base/ManagedObject'],function(q,M){"use strict";var Q=M.extend("sap.ui.dt.test.report.QUnit",{metadata:{library:"sap.ui.dt",properties:{data:{type:"object"}}},init:function(){if(!QUnit){throw new Error("QUnit is required for this report.");}},setData:function(d){if(d){var c=d.children;c.forEach(function(g){this._createModule(g);},this);}this.setProperty("data",d);},_createModule:function(g){QUnit.module(g.message);g.children.forEach(function(g){this._createTest(g);},this);},_createTest:function(g){QUnit.test(g.name+": "+g.message,function(a){g.children.forEach(function(g){this._createAssertion(g);},this);}.bind(this));},_createAssertion:function(g){if(g.children.length>0){g.children.forEach(function(t){assert.ok(t.result,g.name+": "+t.message);});}else{assert.ok(true,g.name+": "+g.message);}}});return Q;},true);
