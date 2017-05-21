/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/dt/DesignTimeMetadata'],function(q,D){"use strict";var A=D.extend("sap.ui.dt.AggregationDesignTimeMetadata",{metadata:{library:"sap.ui.dt"}});A.prototype.getMoveAction=function(m){var d=this.getData();if(d.actions&&d.actions.move){var M=d.actions.move;if(typeof(M)==="function"){return M.apply(null,arguments);}return M;}};return A;},true);
