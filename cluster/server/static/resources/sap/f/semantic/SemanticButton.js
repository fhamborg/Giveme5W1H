/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["./SemanticControl","./SemanticConfiguration","sap/m/Button","sap/m/OverflowToolbarButton"],function(S,a,B,O){"use strict";var b=S.extend("sap.f.semantic.SemanticButton",{metadata:{library:"sap.f","abstract":true,properties:{enabled:{type:"boolean",group:"Behavior",defaultValue:true}},events:{press:{}}}});b.prototype._getControl=function(){var c=this.getAggregation('_control'),C=this._getConfiguration(),o,n;if(!C){return null;}if(!c){o=C&&C.constraints==="IconOnly"?O:B;n=this._createInstance(o);n.applySettings(C.getSettings());if(typeof C.getEventDelegates==="function"){n.addEventDelegate(C.getEventDelegates(n));}this.setAggregation('_control',n,true);c=this.getAggregation('_control');}return c;};b.prototype._createInstance=function(c){return new c({id:this.getId()+"-button",press:jQuery.proxy(this.firePress,this)});};return b;},false);
