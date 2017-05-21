/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(function(){"use strict";var W={};W.render=function(r,s){this.startWizardStep(r,s);this.renderWizardStepTitle(r,s);this.renderContent(r,s.getContent());this.endWizardStep(r);};W.startWizardStep=function(r,s){r.write("<article");r.writeAccessibilityState(s,{"labelledby":this.getTitleId(s),"role":"region"});r.writeControlData(s);r.addClass("sapMWizardStep");r.writeClasses();r.write(">");};W.renderWizardStepTitle=function(r,s){r.write("<h3 class='sapMWizardStepTitle' id='"+this.getTitleId(s)+"'>");r.writeEscaped(s.getTitle());r.write("</h3>");};W.getTitleId=function(s){return s.getId()+"-Title";};W.renderContent=function(r,c){c.forEach(r.renderControl);};W.endWizardStep=function(r){r.write("</article>");};return W;},true);
