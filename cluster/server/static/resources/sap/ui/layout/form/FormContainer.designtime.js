/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";function _(f){return f.getFormElements().every(function(F){return F.getVisible()===false;});}return{aggregations:{formElements:{domRef:function(f){var d=f.getDomRef();if(!d&&f.getFormElements().length===0||_(f)){var h=f.getTitle()||f.getToolbar();if(h){return h.getDomRef();}}else{return d;}}}}};},false);
