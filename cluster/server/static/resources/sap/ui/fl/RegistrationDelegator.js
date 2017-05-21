/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["sap/ui/fl/FlexController","sap/ui/core/Component","sap/ui/fl/registry/ChangeHandlerRegistration","sap/ui/fl/ChangePersistenceFactory","sap/ui/core/mvc/Controller","sap/ui/core/mvc/XMLView"],function(F,C,a,b,M,X){"use strict";var R={};R.registerChangesInComponent=function(){C._fnOnInstanceCreated=F.getChangesAndPropagate.bind(F);};R.registerChangeHandlers=function(){a.getChangeHandlersOfLoadedLibsAndRegisterOnNewLoadedLibs();};R.registerLoadComponentEventHandler=function(){C._fnLoadComponentCallback=b._onLoadComponent.bind(b);};R.registerExtensionProvider=function(){M.registerExtensionProvider("sap.ui.fl.PreprocessorImpl");};R.registerXMLPreprocessor=function(){if(X.registerPreprocessor){X.registerPreprocessor("viewxml","sap.ui.fl.XmlPreprocessorImpl",true);}};R.registerAll=function(){R.registerChangeHandlers();R.registerLoadComponentEventHandler();R.registerExtensionProvider();R.registerChangesInComponent();R.registerXMLPreprocessor();};return R;},true);
