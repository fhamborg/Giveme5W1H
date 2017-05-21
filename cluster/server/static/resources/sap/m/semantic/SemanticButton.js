/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/m/semantic/SemanticControl','sap/m/Button','sap/m/semantic/SemanticOverflowToolbarButton'],function(S,B,a){"use strict";var b=S.extend("sap.m.semantic.SemanticButton",{metadata:{library:"sap.m","abstract":true,properties:{enabled:{type:"boolean",group:"Behavior",defaultValue:true}},events:{press:{}}}});b.prototype._getControl=function(){var c=this.getAggregation('_control');if(!c){var C=this._getConfiguration()&&this._getConfiguration().constraints==="IconOnly"?a:B;var n=this._createInstance(C);n.applySettings(this._getConfiguration().getSettings());if(typeof this._getConfiguration().getEventDelegates==="function"){n.addEventDelegate(this._getConfiguration().getEventDelegates(n));}this.setAggregation('_control',n,true);c=this.getAggregation('_control');}return c;};b.prototype._createInstance=function(c){return new c({id:this.getId()+"-button",press:jQuery.proxy(this.firePress,this)});};return b;},true);
