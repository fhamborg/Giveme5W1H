/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','sap/ui/core/Renderer'],function(q,R){'use strict';var I={};I.render=function(r,c){var i,a,b=c.getItems(),d=c._iconTabHeader,e=true;if(d){d._checkTextOnly(b);e=d._bTextOnly;c._bIconOnly=c.checkIconOnly(b);}r.write('<ul');r.writeAttribute('role','listbox');r.writeControlData(c);r.addClass('sapMITBSelectList');if(e){r.addClass('sapMITBSelectListTextOnly');}r.writeClasses();r.write('>');for(i=0;i<b.length;i++){a=b[i];a.renderInSelectList(r,c);}r.write('</ul>');};return I;},true);
