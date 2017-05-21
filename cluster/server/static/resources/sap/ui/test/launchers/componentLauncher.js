/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/ComponentContainer'],function(q,C){"use strict";var $=q,_=false,a=null,b=null;return{start:function(c){if(_){throw"sap.ui.test.launchers.componentLauncher: Start was called twice without teardown";}c.async=true;var p=sap.ui.component(c);_=true;return p.then(function(o){var i=q.sap.uid();b=$('<div id="'+i+'" class="sapUiOpaComponent"></div>');$("body").append(b).addClass("sapUiOpaBodyComponent");a=new C({component:o});a.placeAt(i);});},hasLaunched:function(){return _;},teardown:function(){if(!_){throw"sap.ui.test.launchers.componentLauncher: Teardown has been called but there was no start";}a.destroy();b.remove();_=false;$("body").removeClass("sapUiOpaBodyComponent");}};},true);
