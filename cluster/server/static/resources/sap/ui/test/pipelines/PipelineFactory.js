/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/base/Object'],function(q,U){"use strict";var $=q;return U.extend("sap.ui.test.pipelines.PipelineFactory",{constructor:function(o){this._oOptions=o;},create:function(i){var r=[];if($.isArray(i)){r=i;}else if(i){r=[i];}else{q.sap.log.error(this._oOptions.name+" were defined, but they were neither an array nor a single element: "+i);}r=r.map(function(f){var R;if(f[this._oOptions.functionName]){return f;}else if(typeof f=="function"){R={};R[this._oOptions.functionName]=f;return R;}q.sap.log.error("A "+this._oOptions.name+" was defined, but it is no function and has no '"+this._oOptions.functionName+"' function: "+f);}.bind(this)).filter(function(f){return!!f;});return r;}});});
