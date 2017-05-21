/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['./ComponentMetadata','./library'],function(C,l){"use strict";var V=l.mvc.ViewType;var U=function(c,o){C.apply(this,arguments);};U.prototype=Object.create(C.prototype);U.preprocessClassInfo=function(c){if(c&&typeof c.metadata==="string"){c.metadata={_src:c.metadata};}return c;};U.prototype.getRootView=function(d){return this.getManifestEntry("/sap.ui5/rootView",!d);};U.prototype.getRoutingConfig=function(d){return this.getManifestEntry("/sap.ui5/routing/config",!d);};U.prototype.getRoutes=function(d){return this.getManifestEntry("/sap.ui5/routing/routes",!d);};U.prototype._convertLegacyMetadata=function(s,m){C.prototype._convertLegacyMetadata.call(this,s,m);var u=m["sap.ui5"];var r=u["rootView"]||s["rootView"];if(r){u["rootView"]=r;}var R=u["routing"]||s["routing"];if(R){u["routing"]=R;}if(u["rootView"]&&typeof u["rootView"]==="string"){u["rootView"]={viewName:u["rootView"],type:V.XML};}};return U;},true);
