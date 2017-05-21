/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./UniversalDate','sap/ui/core/Locale','sap/ui/core/LocaleData'],function(q,U,L,a){"use strict";var G=U.extend("sap.ui.core.date.Gregorian",{constructor:function(){this.oDate=this.createDate(Date,arguments);this.sCalendarType=sap.ui.core.CalendarType.Gregorian;}});G.UTC=function(){return Date.UTC.apply(Date,arguments);};G.now=function(){return Date.now();};return G;});
