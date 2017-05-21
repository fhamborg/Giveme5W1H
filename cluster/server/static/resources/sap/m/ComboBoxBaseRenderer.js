/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./ComboBoxTextFieldRenderer','sap/ui/core/Renderer'],function(q,C,R){"use strict";var a=R.extend(C);a.CSS_CLASS_COMBOBOXBASE="sapMComboBoxBase";a.getAccessibilityState=function(c){var A=C.getAccessibilityState.call(this,c);A.expanded=c.isOpen();return A;};a.addOuterClasses=function(r,c){C.addOuterClasses.apply(this,arguments);var b=a.CSS_CLASS_COMBOBOXBASE;r.addClass(b);if(!c.getEnabled()){r.addClass(b+"Disabled");}if(!c.getEditable()){r.addClass(b+"Readonly");}};a.addButtonClasses=function(r,c){C.addButtonClasses.apply(this,arguments);r.addClass(a.CSS_CLASS_COMBOBOXBASE+"Arrow");};return a;},true);
