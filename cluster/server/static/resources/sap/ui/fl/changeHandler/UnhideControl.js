/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Base'],function(q,B){"use strict";var U={};U.applyChange=function(c,C,p){p.modifier.setVisible(C,true);return true;};U.completeChangeContent=function(c,s){var C=c.getDefinition();if(!C.content){C.content={};}};return U;},true);
