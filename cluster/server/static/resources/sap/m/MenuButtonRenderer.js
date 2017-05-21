/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'],function(q){"use strict";var M={};M.CSS_CLASS="sapMMenuBtn";M.render=function(r,m){var w=m.getWidth();r.write("<div");r.writeControlData(m);this.writeAriaAttributes(r,m);r.addClass(M.CSS_CLASS);r.addClass(M.CSS_CLASS+m.getButtonMode());r.writeClasses();if(w!=""||w.toLowerCase()==="auto"){r.addStyle("width",w);}else if(m._isSplitButton()&&m._iInitialWidth){r.addStyle("width",m._iInitialWidth+"px");}r.writeStyles();r.write(">");r.renderControl(m._getButtonControl());r.write("</div>");};M.writeAriaAttributes=function(r,m){r.writeAttribute("aria-haspopup","true");};return M;},true);
