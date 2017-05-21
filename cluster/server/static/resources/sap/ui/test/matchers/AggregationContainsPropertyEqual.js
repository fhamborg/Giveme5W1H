/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Matcher'],function($,M){"use strict";return M.extend("sap.ui.test.matchers.AggregationContainsPropertyEqual",{metadata:{publicMethods:["isMatching"],properties:{aggregationName:{type:"string"},propertyName:{type:"string"},propertyValue:{type:"any"}}},isMatching:function(c){var a,A=this.getAggregationName(),p=this.getPropertyName(),P=this.getPropertyValue(),f=c["get"+$.sap.charToUpperCase(A,0)];if(!f){this._oLogger.error("Control '"+c+"' does not have an aggregation called '"+A+"'");return false;}a=f.call(c);var m=a.some(function(v){var b=v["get"+$.sap.charToUpperCase(p,0)];if(!b){return false;}return b.call(v)===P;});if(!m){this._oLogger.debug("Control '"+c+"' has no property '"+p+"' with the value '"+P+"' in the aggregation '"+A+"'");}return m;}});},true);
