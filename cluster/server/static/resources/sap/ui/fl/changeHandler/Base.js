/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/fl/Utils","jquery.sap.global"],function(U,$){"use strict";var B={};B.setTextInChange=function(c,k,t,T){if(!c.texts){c.texts={};}if(!c.texts[k]){c.texts[k]={};}c.texts[k].value=t;c.texts[k].type=T;};return B;},true);
