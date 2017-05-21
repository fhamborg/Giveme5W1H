/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./ListItemBaseRenderer','sap/ui/core/Renderer'],function(q,L,R){"use strict";var T=R.extend(L);T.renderLIAttributes=function(r,l){r.addClass("sapMTreeItemBase");if(!l.isTopLevel()){r.addClass("sapMTreeItemBaseChildren");}var i=l._getLevelIndentCSS();if(sap.ui.getCore().getConfiguration().getRTL()){r.addStyle("padding-right",i+"rem");}else{r.addStyle("padding-left",i+"rem");}};T.renderContentFormer=function(r,l){this.renderHighlight(r,l);this.renderExpander(r,l);this.renderMode(r,l,-1);};T.renderExpander=function(r,l){var e=l._getExpanderControl();if(e){r.renderControl(e);}};T.getAriaRole=function(l){return"treeitem";};T.getAccessibilityState=function(l){var a=L.getAccessibilityState.call(this,l);a.level=l.getLevel()+1;a.expanded=l.getExpanded();return a;};return T;},true);
