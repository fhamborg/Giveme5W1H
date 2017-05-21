/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['./SemanticButton','./SemanticControl','sap/m/ButtonType'],function(S,a,B){"use strict";var b=S.extend("sap.f.semantic.SemanticToggleButton",{metadata:{library:"sap.f","abstract":true,properties:{pressed:{type:"boolean",group:"Data",defaultValue:false}}}});b.prototype._onTap=function(e){e.setMarked();if(this.getEnabled()){this.setPressed(!this.getPressed());this.firePress({pressed:this.getPressed()});}};b.prototype._onKeydown=function(e){if(e.which===jQuery.sap.KeyCodes.SPACE||e.which===jQuery.sap.KeyCodes.ENTER){this._onTap(e);}};b.prototype._applyProperty=function(p,v,s){if(p==='pressed'){this._setPressed(v,s);}else{S.prototype._applyProperty.apply(this,arguments);}};b.prototype._setPressed=function(p,s){var o=p?B.Emphasized:B.Transparent;this._getControl().setType(o,s);};b.prototype._createInstance=function(c){var i=new c({id:this.getId()+"-toggleButton"});i.addEventDelegate({ontap:this._onTap,onkeydown:this._onKeydown},this);return i;};return b;},false);
