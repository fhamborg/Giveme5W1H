/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";return{actions:{rename:function(p){if(p.getCustomHeader()){return;}return{changeType:"rename",domRef:function(c){return c.$("title-inner")[0];}};}},aggregations:{headerContent:{domRef:":sap-domref > .sapMPageHeader > .sapMBarRight"},subHeader:{domRef:":sap-domref > .sapMPageSubHeader"},customHeader:{domRef:":sap-domref > .sapMPageHeader"},content:{domRef:":sap-domref > section",actions:{move:"moveControls"}},footer:{domRef:":sap-domref > .sapMPageFooter"},landmarkInfo:{ignore:true}},name:{singular:"PAGE_NAME",plural:"PAGE_NAME_PLURAL"}};},false);
