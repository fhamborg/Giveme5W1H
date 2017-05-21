/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/Renderer','./DatePickerRenderer','./InputBaseRenderer'],function(q,R,D,I){"use strict";var a=R.extend(D);a._getIcon=function(){return"sap-icon://date-time";};a.getDescribedByAnnouncement=function(d){var b=I.getDescribedByAnnouncement.apply(this,arguments);return sap.ui.getCore().getLibraryResourceBundle("sap.m").getText("DATETIMEPICKER_TYPE")+" "+b;};return a;},true);
