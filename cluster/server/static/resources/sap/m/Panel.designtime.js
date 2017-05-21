/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";return{actions:{remove:{changeType:"hideControl"},rename:function(p){if(p.getHeaderToolbar()){return;}return{changeType:"rename",domRef:".sapMPanelHdr"};},reveal:{changeType:"unhideControl"}},aggregations:{headerToolbar:{domRef:":sap-domref > .sapMPanelHeaderTB, :sap-domref > .sapMPanelWrappingDivTb .sapMPanelHeaderTB, :sap-domref > .sapUiDtEmptyHeader"},infoToolbar:{domRef:":sap-domref > .sapMPanelInfoTB, :sap-domref > .sapUiDtEmptyInfoToolbar"},content:{domRef:".sapMPanelContent",show:function(){this.setExpanded(true);},actions:{move:"moveControls"}}},name:{singular:"PANEL_NAME",plural:"PANEL_NAME_PLURAL"}};},false);
