/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./ServiceFactory'],function(q,S){"use strict";var s=Object.create(null);var a=Object.create(null);a.register=function(b,o){s[b]=o;return this;};a.unregister=function(b){delete s[b];return this;};a.get=function(b){return s[b];};return a;},true);
