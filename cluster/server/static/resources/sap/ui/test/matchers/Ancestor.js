/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";return function(a,d){return function(c){if(!a){return true;}var p=c.getParent();while(!d&&p&&p!==a){p=p.getParent();}return p===a;};};},true);
