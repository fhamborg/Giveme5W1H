/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Matcher'],function(q,M){"use strict";return M.extend("sap.ui.test.matchers.PropertyStrictEquals",{metadata:{publicMethods:["isMatching"],properties:{name:{type:"string"},value:{type:"any"}}},isMatching:function(c){var p=this.getName(),i=c.getId(),P=c["get"+q.sap.charToUpperCase(p,0)];if(!P){this._oLogger.error("Control '"+i+"' does not have a property called '"+p+"'");return false;}var v=P.call(c);var m=v===this.getValue();if(!m){this._oLogger.debug("The property '"+p+"' of '"+i+"' has the value '"+v+"' expected '"+this.getValue()+"'");}return m;}});},true);
