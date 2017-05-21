/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/Element','./StandardListItem','./StandardListItemRenderer','sap/ui/core/Renderer','./library','sap/ui/unified/library'],function(q,E,S,a,R,l,u){"use strict";var P=E.extend("sap.m.PlanningCalendarView",{metadata:{library:"sap.m",properties:{key:{type:"string",group:"Data",defaultValue:null},intervalType:{type:"sap.ui.unified.CalendarIntervalType",group:"Appearance",defaultValue:sap.ui.unified.CalendarIntervalType.Hour},description:{type:"string",group:"Data"},intervalsS:{type:"int",group:"Appearance",defaultValue:6},intervalsM:{type:"int",group:"Appearance",defaultValue:8},intervalsL:{type:"int",group:"Appearance",defaultValue:12},showSubIntervals:{type:"boolean",group:"Appearance",defaultValue:false}}}});return P;},true);
