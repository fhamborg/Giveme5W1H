/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(["../_AnnotationHelperBasics","./_AnnotationHelperExpression"],function(B,E){"use strict";var r=/[\\\{\}:]/,a=/\/\$count$/,A={getNavigationBinding:function(p){p=A.getNavigationPath(p);if(r.test(p)){throw new Error("Invalid OData identifier: "+p);}return p?"{"+p+"}":p;},getNavigationPath:function(p){var i;if(!p||p[0]==="@"){return"";}if(a.test(p)){return p.slice(0,-7);}i=p.indexOf("@");if(i>-1){p=p.slice(0,i);}if(p[p.length-1]==="/"){p=p.slice(0,-1);}if(p.indexOf(".")){p=p.split("/").filter(function(s){return s.indexOf(".")<0;}).join("/");}return p;},isMultiple:function(p,d){var i;if(!p||p[0]==="@"){return false;}if(a.test(p)){return true;}i=p.indexOf("@");if(i>-1){p=p.slice(0,i);}if(p[p.length-1]!=="/"){p+="/";}p="/"+d.schemaChildName+"/"+p+"$isCollection";return d.context.getObject(p)===true;},value:function(R,d){var p=d.context.getPath();if(p.slice(-1)==="/"){p=p.slice(0,-1);}return E.getExpression({asExpression:false,model:d.context.getModel(),path:p,value:R});}};return A;},true);
