/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["jquery.sap.global","sap/ui/base/ManagedObject","sap/ui/test/_LogCollector"],function($,M,_){"use strict";var a=M.extend("sap.ui.test.matchers.Matcher",{metadata:{publicMethods:["isMatching"]},constructor:function(){this._oLogger=$.sap.log.getLogger(this.getMetadata().getName(),_.DEFAULT_LEVEL_FOR_OPA_LOGGERS);return M.prototype.constructor.apply(this,arguments);},isMatching:function(c){return true;}});return a;},true);
