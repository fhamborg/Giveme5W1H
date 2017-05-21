/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'],function(q){'use strict';var F={save:function(d,f,s,m,c,b){var a=f+'.'+s;if(typeof b==='undefined'&&c==='utf-8'&&s==='csv'){b=true;}if(b===true&&c==='utf-8'){d='\ufeff'+d;}if(window.Blob){var t='data:'+m;if(c){t+=';charset='+c;}var B=new window.Blob([d],{type:t});if(window.navigator.msSaveOrOpenBlob){window.navigator.msSaveOrOpenBlob(B,a);}else{var u=window.URL||window.webkitURL;var e=u.createObjectURL(B);var l=window.document.createElement('a');if('download'in l){var $=q(document.body);var g=q(l).attr({download:a,href:e,style:'display:none'});$.append(g);g.get(0).click();g.remove();}else{d=encodeURI(d);var w=window.open(t+","+d);if(!w){throw new Error("Could not download file. A popup blocker might be active.");}}}}}};return F;},true);
