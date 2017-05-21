/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["./Control"],function(C){"use strict";var a=function(){var c;if(!(this instanceof C)){return;}function o(e){e.stopPropagation();if(e.srcControl!==this){return;}e.preventDefault();this._oContextMenu.openAsContextMenu(e,this);}c={oncontextmenu:o};this.setContextMenu=function(b){if(b==null&&this.getContextMenu()){this._oContextMenu=null;this.removeEventDelegate(c,this);return;}else if(!b||!b.getMetadata||!b.getMetadata().isInstanceOf("sap.ui.core.IContextMenu")){return;}if(!this._oContextMenu){this.addEventDelegate(c,this);}this._oContextMenu=b;};this.getContextMenu=function(){return this._oContextMenu;};};return a;},true);
