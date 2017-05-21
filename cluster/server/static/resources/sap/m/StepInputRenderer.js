/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";var S={};S.render=function(r,c){var i=c._getIncrementButton(),d=c._getDecrementButton(),I=c._getInput(),w=c.getWidth(),e=c.getEnabled(),E=c.getEditable();r.write("<div");e&&E&&r.write(" tabindex='-1'");r.addStyle("width",w);r.writeStyles();r.writeControlData(c);r.writeAccessibilityState(c);r.addClass("sapMStepInput");r.addClass("sapMStepInput-CTX");!e&&r.addClass("sapMStepInputReadOnly");!E&&r.addClass("sapMStepInputDisabled");r.writeClasses();r.write(">");if(E){this.wrapButtons(r,d,["sapMStepInputBtnDecrease"]);}r.renderControl(I);if(E){this.wrapButtons(r,i,["sapMStepInputBtnIncrease"]);}r.write("</div>");};S.wrapButtons=function(r,c,C){r.write("<div tabindex='-1'");r.addClass("sapMStepInputBtnWrapper");C.forEach(function(s){r.addClass(s);});r.writeClasses();r.write(">");r.renderControl(c);r.write("</div>");};return S;},true);
