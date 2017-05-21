/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Matcher','./AggregationLengthEquals'],function($,M,A){"use strict";var a=new A({length:0});return M.extend("sap.ui.test.matchers.AggregationEmpty",{metadata:{publicMethods:["isMatching"],properties:{name:{type:"string"}}},isMatching:function(c){a.setName(this.getName());return a.isMatching(c);}});},true);
