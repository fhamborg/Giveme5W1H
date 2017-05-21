/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['./RenderManager'],function(R){"use strict";var a=R.RenderPrefixes;var H={render:function(r,c){r.write("<div id=\""+a.Dummy+c.getId()+"\" style=\"display:none\">");r.write("</div>");}};return H;},true);
