/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/core/mvc/Controller","sap/ui/fl/support/apps/contentbrowser/utils/ErrorUtils"],function(C,E){"use strict";return C.extend("sap.ui.fl.support.apps.contentbrowser.controller.Layers",{onLayerSelected:function(e){var s=e.getSource();var l=s.getBindingContextPath().substring(1);var L=this.getView().getModel("layers").getData();var a=L[l].name;var r=sap.ui.core.UIComponent.getRouterFor(this);r.navTo("LayerContentMaster",{"layer":a});},handleMessagePopoverPress:function(e){var s=e.getSource();E.handleMessagePopoverPress(s);}});});
