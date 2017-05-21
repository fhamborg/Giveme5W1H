/*
 * ! UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./library','sap/ui/core/Item'],function(q,l,I){"use strict";var P=I.extend("sap.m.P13nFilterItem",{metadata:{library:"sap.m",properties:{operation:{type:"string",group:"Misc",defaultValue:null},value1:{type:"string",group:"Misc",defaultValue:null},value2:{type:"string",group:"Misc",defaultValue:null},columnKey:{type:"string",group:"Misc",defaultValue:null},exclude:{type:"boolean",group:"Misc",defaultValue:false}}}});P.prototype.setOperation=function(o){return this.setProperty("operation",o,true);};P.prototype.setColumnKey=function(k){return this.setProperty("columnKey",k,true);};P.prototype.setValue1=function(k){return this.setProperty("value1",k,true);};P.prototype.setValue2=function(k){return this.setProperty("value2",k,true);};P.prototype.setExclude=function(k){return this.setProperty("exclude",k,true);};return P;},true);
