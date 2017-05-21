/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/Renderer','./DatePickerRenderer'],function(q,R,D){"use strict";var a=R.extend(D);a.writeInnerValue=function(r,c){if(c._bValid){r.writeAttributeEscaped("value",c._formatValue(c.getDateValue(),c.getSecondDateValue()));}else{r.writeAttributeEscaped("value",c.getValue());}};return a;},true);
