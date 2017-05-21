/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./TreeItemBase','./library','sap/ui/core/EnabledPropagator','sap/ui/core/IconPool','sap/ui/core/Icon','./StandardListItem'],function(q,T,l,E,I,a,S){"use strict";var b=T.extend("sap.m.StandardTreeItem",{metadata:{library:"sap.m",properties:{title:{type:"string",group:"Misc",defaultValue:""},icon:{type:"sap.ui.core.URI",group:"Misc",defaultValue:null}}}});b.prototype._getIconControl=function(){var u=this.getIcon();if(this._oIconControl){this._oIconControl.setSrc(u);return this._oIconControl;}this._oIconControl=I.createControlByURI({id:this.getId()+"-icon",src:u,useIconTooltip:false,noTabStop:true},sap.m.Image).setParent(this,null,true).addStyleClass("sapMSTIIcon");return this._oIconControl;};b.prototype.getContentAnnouncement=function(){var A="",i=I.getIconInfo(this.getIcon())||{};A+=(i.text||i.name||"")+" ";A+=this.getTitle()+" ";return A;};b.prototype.exit=function(){T.prototype.exit.apply(this,arguments);this.destroyControls(["Icon"]);};return b;},true);
