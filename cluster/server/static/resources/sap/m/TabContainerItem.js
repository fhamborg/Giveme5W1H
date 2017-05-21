/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/core/Element','sap/ui/core/Control'],function(E,C){"use strict";var T=E.extend("sap.m.TabContainerItem",{metadata:{library:"sap.ui.core",properties:{name:{type:"string",group:"Misc",defaultValue:""},key:{type:"string",group:"Data",defaultValue:null},modified:{type:"boolean",group:"Misc",defaultValue:false}},aggregations:{content:{type:"sap.ui.core.Control",multiple:true,defaultValue:null}},events:{itemPropertyChanged:{parameters:{itemChanged:{type:"sap.m.TabContainerItem"},propertyKey:{type:"string"},propertyValue:{type:"any"}}}}}});T.prototype.setProperty=function(n,v,s){if(n==="modified"){s=true;}this.fireItemPropertyChanged({itemChanged:this,propertyKey:n,propertyValue:v});return E.prototype.setProperty.call(this,n,v,s);};return T;});
