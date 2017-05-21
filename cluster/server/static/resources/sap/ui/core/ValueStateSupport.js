/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Element','./library'],function(q,E,l){"use strict";var V=l.ValueState;var a={};var t=null;var e=function(){if(!t){t={};var r=sap.ui.getCore().getLibraryResourceBundle("sap.ui.core");t[V.Error]=r.getText("VALUE_STATE_ERROR");t[V.Warning]=r.getText("VALUE_STATE_WARNING");t[V.Success]=r.getText("VALUE_STATE_SUCCESS");}};a.enrichTooltip=function(o,T){if(!T&&o.getTooltip()){return undefined;}var s=a.getAdditionalText(o);if(s){return(T?T+" - ":"")+s;}return T;};a.getAdditionalText=function(v){var s=null;if(v&&v.getValueState){s=v.getValueState();}else if(V[v]){s=v;}if(s&&(s!=V.None)){e();return t[s];}return null;};a.formatValueState=function(s){switch(s){case 1:return V.Warning;case 2:return V.Success;case 3:return V.Error;default:return V.None;}};return a;},true);
