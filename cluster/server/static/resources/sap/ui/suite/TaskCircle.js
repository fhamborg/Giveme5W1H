/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/Control','sap/ui/core/EnabledPropagator','./library'],function(q,C,E,l){"use strict";var T=l.TaskCircleColor;var a=C.extend("sap.ui.suite.TaskCircle",{metadata:{library:"sap.ui.suite",properties:{value:{type:"int",group:"Misc",defaultValue:0},maxValue:{type:"int",group:"Misc",defaultValue:100},minValue:{type:"int",group:"Misc",defaultValue:0},color:{type:"sap.ui.suite.TaskCircleColor",group:"Misc",defaultValue:T.Gray}},associations:{ariaLabelledBy:{type:"sap.ui.core.Control",multiple:true,singularName:"ariaLabelledBy"},ariaDescribedBy:{type:"sap.ui.core.Control",multiple:true,singularName:"ariaDescribedBy"}},events:{press:{}}}});E.call(a.prototype);a.prototype.init=function(){};a.prototype.onclick=function(e){this.firePress({});e.preventDefault();e.stopPropagation();};a.prototype.focus=function(){var d=this.getDomRef();if(d){d.focus();}};return a;});
