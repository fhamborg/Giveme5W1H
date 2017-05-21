/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/core/Element","sap/ui/dt/ElementUtil"],function(E,a){"use strict";var O={};var o={};O.getOverlay=function(e){var b=a.getElementInstance(e);if(b){b=a.fixComponentContainerElement(b);b=a.fixComponentParent(b);if(b){var i=b.getId();return o[i];}}};O.register=function(e,b){var i=g(e);o[i]=b;};O.deregister=function(e){var i=g(e);delete o[i];};O.hasOverlays=function(){return!jQuery.isEmptyObject(o);};function g(e){return(e instanceof E)?e.getId():e;}return O;},true);
