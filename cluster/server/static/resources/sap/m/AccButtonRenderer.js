/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./ButtonRenderer','sap/ui/core/Renderer'],function(q,B,R){"use strict";var A=R.extend(B);A.renderAccessibilityAttributes=function(r,c){if(c.getTabIndex()){r.writeAttribute("tabindex",c.getTabIndex());}if(c.getAriaHidden()){r.writeAttribute("aria-hidden",c.getAriaHidden());}};return A;},true);
