/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/core/routing/Target','./async/Target','./sync/Target'],function(T,a,s){"use strict";var M=T.extend("sap.m.routing.Target",{constructor:function(o,v,p,t){this._oTargetHandler=t;function c(){if(jQuery.sap.getUriParameters().get("sap-ui-xx-asyncRouting")==="true"){jQuery.sap.log.warning("Activation of async view loading in routing via url parameter is only temporarily supported and may be removed soon","MobileTarget");return true;}return false;}if(o._async===undefined){o._async=c();}T.prototype.constructor.apply(this,arguments);var b=o._async?a:s;this._super={};for(var f in b){this._super[f]=this[f];this[f]=b[f];}}});return M;},true);
