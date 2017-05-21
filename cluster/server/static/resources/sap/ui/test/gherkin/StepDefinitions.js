/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["jquery.sap.global","sap/ui/base/Object"],function($,U){"use strict";var S=U.extend("sap.ui.test.gherkin.StepDefinitions",{constructor:function(){U.apply(this,arguments);this._aDefinitions=[];this.init();},init:function(){},closeApplication:function(){},register:function(r,f){if($.type(r)!=="regexp"){throw new Error("StepDefinitions.register: parameter 'rRegex' must be a valid RegExp object");}if($.type(f)!=="function"){throw new Error("StepDefinitions.register: parameter 'fnFunc' must be a valid Function");}this._aDefinitions.unshift({generateTestStep:function(s){var m=s.text.match(r);if(!m){return{isMatch:false};}var p=m.slice(1);if(s.data){p.push($.extend(true,[],s.data));}return{isMatch:true,text:s.text,regex:r,parameters:p,func:f};}});},_generateTestStep:function(s){for(var i=0;i<this._aDefinitions.length;++i){var d=this._aDefinitions[i];var t=d.generateTestStep(s);if(t.isMatch){return t;}}return{isMatch:false,text:"(NOT FOUND) "+s.text};}});return S;},true);
