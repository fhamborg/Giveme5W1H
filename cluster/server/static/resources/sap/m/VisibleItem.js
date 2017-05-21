/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./library','sap/ui/core/Item'],function(q,l,I){"use strict";var V=I.extend("sap.m.VisibleItem",{metadata:{library:"sap.m",properties:{visible:{type:"boolean",group:"Behavior",defaultValue:true}}}});V.prototype._getRefs=function(){var p=this.getParent(),$,t=this;if(p&&p.$("content")){$=p.$("content").find("li").filter(function(){return q(this).html()===t.getText();});}return $;};V.prototype.setVisible=function(v){if(this.getVisible()===v){return;}var $=this._getRefs();if($){if(v){$.removeClass('TPSliderItemHidden');}else{$.addClass('TPSliderItemHidden');}}return this.setProperty('visible',v,true);};return V;},false);
