/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define("sap/ui/fl/support/apps/contentbrowser/utils/HtmlEscapeUtils",function(){"use strict";var H={};H.sUnescapedSlash="/";H.sEscapedSlash="%2F";H.escapeSlashes=function(s){return this._replaceAll(s,H.sUnescapedSlash,H.sEscapedSlash);};H.unescapeSlashes=function(s){return this._replaceAll(s,H.sEscapedSlash,H.sUnescapedSlash);};H._replaceAll=function(s,S,r){if(s.indexOf(S)===-1){return s;}return this._replaceAll(s.replace(S,r),S,r);};return H;});
