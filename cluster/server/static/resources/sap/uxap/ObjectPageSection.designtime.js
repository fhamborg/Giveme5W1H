/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";return{name:{singular:function(){return sap.uxap.i18nModel.getResourceBundle().getText("SECTION_CONTROL_NAME");},plural:function(){return sap.uxap.i18nModel.getResourceBundle().getText("SECTION_CONTROL_NAME_PLURAL");}},actions:{remove:{changeType:"stashControl"},reveal:{changeType:"unstashControl"}}};},false);
