/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./ComboBoxBaseRenderer','sap/ui/core/Renderer'],function(q,C,R){"use strict";var a=R.extend(C);a.CSS_CLASS_COMBOBOX="sapMComboBox";a.addOuterClasses=function(r,c){C.addOuterClasses.apply(this,arguments);r.addClass(a.CSS_CLASS_COMBOBOX);};a.addInnerClasses=function(r,c){C.addInnerClasses.apply(this,arguments);r.addClass(a.CSS_CLASS_COMBOBOX+"Inner");};a.addButtonClasses=function(r,c){C.addButtonClasses.apply(this,arguments);r.addClass(a.CSS_CLASS_COMBOBOX+"Arrow");};a.addPlaceholderClasses=function(r,c){C.addPlaceholderClasses.apply(this,arguments);r.addClass(a.CSS_CLASS_COMBOBOX+"Placeholder");};return a;},true);
