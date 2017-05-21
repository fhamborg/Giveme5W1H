/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";var c;sap.ui.getCore().registerPlugin({startPlugin:function(C){c=C;}});return{getAllControls:function(C){var o,p,r=[],a=this.getCoreElements();for(p in a){if(!a.hasOwnProperty(p)){continue;}o=a[p];if(this.checkControlType(o,C)){r.push(o);}}return r;},checkControlType:function(C,f){if(f){return C instanceof f;}else{return true;}},getCoreElements:function(){var e={};if(!c){return e;}return c.mElements||e;},isUIDirty:function(){return c&&c.getUIDirty();}};},true);
