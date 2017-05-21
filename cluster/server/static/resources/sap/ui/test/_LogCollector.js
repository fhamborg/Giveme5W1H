/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/base/Object","jquery.sap.global"],function(U,$){"use strict";var s;var m="sap.ui.test._LogCollector";var d=$.sap.log.Level.DEBUG;var _=$.sap.log.getLogger(m,d);var a=U.extend(m,{constructor:function(){this._aLogs=[];this._oListener={onLogEntry:function(l){if(!$.sap.startsWith(l.component,"sap.ui.test")){return;}var L=l.message+" - "+l.details+" "+l.component;var b=this._aLogs;b.push(L);if(b.length>500){b.length=0;_.error("Opa has received 500 logs without a consumer - "+"maybe you loaded Opa.js inside of an IFrame? "+"The logs are now cleared to prevent memory leaking");}}.bind(this)};$.sap.log.addLogListener(this._oListener);},getAndClearLog:function(){var j=this._aLogs.join("\n");this._aLogs.length=0;return j;},destroy:function(){this._aLogs.length=0;$.sap.log.removeLogListener(this._oListener);}});a.getInstance=function(){if(!s){s=new a();}return s;};a.DEFAULT_LEVEL_FOR_OPA_LOGGERS=d;return a;},true);
