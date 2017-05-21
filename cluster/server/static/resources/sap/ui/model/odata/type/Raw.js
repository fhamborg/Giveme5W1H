/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/model/FormatException","sap/ui/model/odata/type/ODataType","sap/ui/model/ParseException","sap/ui/model/ValidateException"],function(F,O,P,V){"use strict";var R=O.extend("sap.ui.model.odata.type.Raw",{constructor:function(f,c){O.apply(this,arguments);if(f!==undefined||c!==undefined||arguments.length>2){throw new Error("Unsupported arguments");}}});R.prototype.formatValue=function(v,t){if(t==="any"){return v;}throw new F("Type 'sap.ui.model.odata.type.Raw' does not support formatting");};R.prototype.getName=function(){return"sap.ui.model.odata.type.Raw";};R.prototype.parseValue=function(){throw new P("Type 'sap.ui.model.odata.type.Raw' does not support parsing");};R.prototype.validateValue=function(){throw new V("Type 'sap.ui.model.odata.type.Raw' does not support validating");};return R;});
