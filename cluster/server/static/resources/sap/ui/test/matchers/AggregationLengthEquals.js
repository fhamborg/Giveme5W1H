/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Matcher'],function($,M){"use strict";return M.extend("sap.ui.test.matchers.AggregationLengthEquals",{metadata:{publicMethods:["isMatching"],properties:{name:{type:"string"},length:{type:"int"}}},isMatching:function(c){var a=this.getName(),A=c["get"+$.sap.charToUpperCase(a,0)];if(!A){this._oLogger.error("Control '"+c+"' does not have an aggregation called '"+a+"'");return false;}var i=A.call(c).length;var e=this.getLength();var I=i===e;if(!I){this._oLogger.debug("Control '"+c+"' has "+i+" Objects in the aggregation '"+a+"' but it should have "+e);}return I;}});},true);
