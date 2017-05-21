/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["jquery.sap.global","sap/ui/fl/FlexController","sap/ui/fl/Utils"],function(q,F,U){"use strict";var a={};a._instanceCache={};a.create=function(c){var f=a._instanceCache[c];if(!f){f=new F(c);a._instanceCache[c]=f;}return f;};a.createForControl=function(c){var C=U.getComponentClassName(c);return a.create(C);};return a;},true);
