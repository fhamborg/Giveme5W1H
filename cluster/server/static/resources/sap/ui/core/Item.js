/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['./Element','./library'],function(E,l){"use strict";var T=l.TextDirection;var I=E.extend("sap.ui.core.Item",{metadata:{library:"sap.ui.core",properties:{text:{type:"string",group:"Misc",defaultValue:""},enabled:{type:"boolean",group:"Misc",defaultValue:true},textDirection:{type:"sap.ui.core.TextDirection",group:"Misc",defaultValue:T.Inherit},key:{type:"string",group:"Data",defaultValue:null}}}});return I;});
