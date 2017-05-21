/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["jquery.sap.global","sap/ui/test/_LogCollector"],function($,_){"use strict";var l=$.sap.log.getLogger("sap.ui.test.matchers.Properties",_.DEFAULT_LEVEL_FOR_OPA_LOGGERS);return function(p){return function(c){var i=true;$.each(p,function(P,o){var f=c["get"+$.sap.charToUpperCase(P,0)];if(!f){i=false;l.error("Control '"+c.sId+"' does not have a property called: '"+P+"'");return false;}var C=f.call(c);if(o instanceof RegExp){i=o.test(C);}else{i=C===o;}if(!i){l.debug("The property '"+P+"' of the control '"+c+"' "+"is '"+C+"', expected '"+o+"'");return false;}});return i;};};},true);
