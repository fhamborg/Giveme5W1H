/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Matcher'],function($,M){"use strict";return M.extend("sap.ui.test.matchers.Visible",{isMatching:function(c){if(!c.getDomRef()){this._oLogger.debug("The control "+c+" is not rendered");return false;}var v=c.$().is(":visible");if(!v){this._oLogger.debug("The control "+c+" is not visible");}return v;}});},true);
