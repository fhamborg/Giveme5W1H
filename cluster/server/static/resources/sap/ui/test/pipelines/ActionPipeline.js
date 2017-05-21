/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/base/Object','./PipelineFactory'],function($,U,P){"use strict";var p=new P({name:"Action",functionName:"executeOn"});return U.extend("sap.ui.test.matcherPipeline",{process:function(o){var c,C=o.control;var a=p.create(o.actions);if(!$.isArray(C)){c=[C];}else{c=C;}c.forEach(function(b){a.forEach(function(A){A.executeOn(b);});});}});});
