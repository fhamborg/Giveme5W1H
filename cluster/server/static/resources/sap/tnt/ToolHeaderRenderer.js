/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/core/Renderer','sap/m/OverflowToolbarRenderer','sap/m/BarInPageEnabler'],function(R,O,B){"use strict";var T=R.extend(O);T.renderBarContent=function(r,t){var o=false;var i;t._getVisibleContent().forEach(function(c){i=c.getMetadata().getName()=='sap.tnt.ToolHeaderUtilitySeparator';if(!o&&i&&t._getOverflowButtonNeeded()){T.renderOverflowButton(r,t);o=true;}B.addChildClassTo(c,t);r.renderControl(c);});if(!o&&t._getOverflowButtonNeeded()){T.renderOverflowButton(r,t);}};return T;},true);
