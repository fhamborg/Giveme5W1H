/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/base/Object'],function(B){"use strict";var S=B.extend("sap.ui.model.Sorter",{constructor:function(p,d,g,c){if(typeof p==="object"){var s=p;p=s.path;d=s.descending;g=s.group;c=s.comparator;}this.sPath=p;var i=this.sPath.indexOf(">");if(i>0){jQuery.sap.log.error("Model names are not allowed in sorter-paths: \""+this.sPath+"\"");this.sPath=this.sPath.substr(i+1);}this.bDescending=d;this.vGroup=g;if(typeof g=="boolean"&&g){this.fnGroup=function(C){return C.getProperty(this.sPath);};}if(typeof g=="function"){this.fnGroup=g;}this.fnCompare=c;},getGroup:function(c){var g=this.fnGroup(c);if(typeof g==="string"||typeof g==="number"||typeof g==="boolean"||g==null){g={key:g};}return g;},getGroupFunction:function(){return this.fnGroup&&this.fnGroup.bind(this);}});S.defaultComparator=function(a,b){if(a==b){return 0;}if(b==null){return-1;}if(a==null){return 1;}if(typeof a=="string"&&typeof b=="string"){return a.localeCompare(b);}if(a<b){return-1;}if(a>b){return 1;}return 0;};return S;});
