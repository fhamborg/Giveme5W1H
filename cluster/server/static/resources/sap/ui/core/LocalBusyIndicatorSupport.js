/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Control'],function(q,C){"use strict";var L=function(){if(this===C.prototype){this.setDelay=this.setBusyIndicatorDelay;}else{q.sap.log.error("Only controls can use the LocalBusyIndicator",this);}};return L;},true);
