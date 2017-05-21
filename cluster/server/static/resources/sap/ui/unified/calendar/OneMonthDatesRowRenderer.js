/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/Renderer','sap/ui/unified/calendar/CalendarUtils','sap/ui/core/date/UniversalDate','./MonthRenderer','./DatesRowRenderer'],function(q,R,C,U,M,D){"use strict";var O=R.extend(D);O.getClass=function(d){if(d.iMode<2){return M.getClass(d);}else{return D.getClass(d);}};O.renderDays=function(r,d,o){if(d.iMode<2){M.renderDays(r,d,o);}else{D.renderDays(r,d,o);}};return O;},true);
