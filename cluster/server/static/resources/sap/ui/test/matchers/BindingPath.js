/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Matcher'],function($,M){"use strict";return M.extend("sap.ui.test.matchers.BindingPath",{metadata:{publicMethods:["isMatching"],properties:{path:{type:"string"},modelName:{type:"string"}}},isMatching:function(c){var b;if(!this.getPath()){throw new Error(this+" the path needs to be a not empty string");}if(this.getModelName()){b=c.getBindingContext(this.getModelName());}else{b=c.getBindingContext();}if(!b){this._oLogger.debug("The control "+c+" has no binding context for the model "+this.getModelName());return false;}var r=this.getPath()===b.getPath();if(!r){this._oLogger.debug("The control "+c+" does not "+"have a matching binding context expected "+this.getPath()+" but got "+b.getPath());}return r;}});},true);
