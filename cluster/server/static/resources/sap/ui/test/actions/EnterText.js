/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Action','sap/ui/Device'],function($,A,D){"use strict";return A.extend("sap.ui.test.actions.EnterText",{metadata:{properties:{text:{type:"string"},clearTextFirst:{type:"boolean",defaultValue:true}},publicMethods:["executeOn"]},executeOn:function(c){var a=this.$(c),o=a[0];if(!o){return;}if(this.getText()===undefined||(!this.getClearTextFirst()&&!this.getText())){$.sap.log.error("Please provide a text for this EnterText action",this._sLogPrefix);return;}var u=this.getUtils();this._tryOrSimulateFocusin(a,c);if(this.getClearTextFirst()){u.triggerKeydown(o,$.sap.KeyCodes.DELETE);u.triggerKeyup(o,$.sap.KeyCodes.DELETE);a.val("");u.triggerEvent("input",o);}this.getText().split("").forEach(function(C){u.triggerCharacterInput(o,C);u.triggerEvent("input",o);});this._simulateFocusout(o);u.triggerEvent("search",o);}});},true);
