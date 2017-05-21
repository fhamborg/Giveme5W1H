/*!
* UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
*/
sap.ui.define(["sap/ui/fl/registry/ChangeRegistry"],function(C){"use strict";var a={getChangeHandlersOfLoadedLibsAndRegisterOnNewLoadedLibs:function(){var t=this;var c=sap.ui.getCore();var A=c.getLoadedLibraries();jQuery.each(A,function(l,L){if(L.extensions&&L.extensions.flChangeHandlers){t.registerFlexChangeHandlers(L.extensions.flChangeHandlers);}});c.attachLibraryChanged(this.handleLibraryRegistrationAfterFlexLibraryIsLoaded.bind(this));},registerFlexChangeHandlers:function(f){if(f){var c=C.getInstance();c.registerControlsForChanges(f);}},handleLibraryRegistrationAfterFlexLibraryIsLoaded:function(l){if(l.getParameter("operation")==="add"){var L=l.getParameter("metadata");if(L&&L.extensions&&L.extensions.flChangeHandlers){var f=L.extensions.flChangeHandlers;this.registerFlexChangeHandlers(f);}}}};return a;},true);
