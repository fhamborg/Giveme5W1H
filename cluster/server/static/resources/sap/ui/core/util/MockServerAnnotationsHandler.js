/*
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/Device','sap/ui/core/util/MockServer','sap/ui/model/odata/ODataModel','jquery.sap.xml'],function(q,D,M,O){"use strict";return{parse:function(m,s){if(!this._index){this._index=0;}var u="/annotationhandler"+this._index++ +"/";var o=new M({rootUri:u,requests:[{method:"GET",path:new RegExp("\\$metadata"),response:function(x){x.respond(200,{"Content-Type":"application/xml;charset=utf-8"},s);}}]});o.start();var a={annotationURI:[u+"$metadata"],json:true};var b=new O(u,a);var A=b.getServiceAnnotations();o.destroy();return A;}};},true);
