/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'],function(q){"use strict";return{_getViewWithGlobalId:function(o){function c(){return sap.ui.view(o);}var v,V;if(!o){q.sap.log.error("the oOptions parameter of getView is mandatory",this);}else{if(o.async===undefined){o.async=true;}V=o.viewName;this._checkViewName(V);v=this._oViews[V];}if(v){return v;}if(this._oComponent){v=this._oComponent.runAsOwner(c);}else{v=c();}this._oViews[V]=v;v.loaded().then(function(v){this.fireCreated({view:v,viewOptions:o});}.bind(this));return v;}};});
