/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["jquery.sap.global","sap/ui/fl/changeHandler/HideControl","sap/ui/fl/changeHandler/UnhideControl","sap/ui/fl/changeHandler/StashControl","sap/ui/fl/changeHandler/UnstashControl","sap/ui/fl/changeHandler/MoveElements","sap/ui/fl/changeHandler/MoveControls","sap/ui/fl/changeHandler/PropertyChange","sap/ui/fl/changeHandler/PropertyBindingChange"],function(q,H,U,S,a,M,b,P,c){"use strict";var d={hideControl:{changeType:"hideControl",changeHandler:H},unhideControl:{changeType:"unhideControl",changeHandler:U},stashControl:{changeType:"stashControl",changeHandler:S},unstashControl:{changeType:"unstashControl",changeHandler:a},moveElements:{changeType:"moveElements",changeHandler:M},moveControls:{changeType:"moveControls",changeHandler:b},propertyChange:{changeType:"propertyChange",changeHandler:P},propertyBindingChange:{changeType:"propertyBindingChange",changeHandler:c}};return d;},true);
