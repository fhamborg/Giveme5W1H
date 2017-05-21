/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./Sorter'],function(q,S){"use strict";var c={};c.apply=function(d,s,g,G){var t=this,e=[],C=[],v,o;if(!s||s.length==0){return d;}for(var j=0;j<s.length;j++){o=s[j];C[j]=o.fnCompare||S.defaultComparator;q.each(d,function(i,r){v=g(r,o.sPath);if(typeof v=="string"){v=v.toLocaleUpperCase();}if(!e[j]){e[j]=[];}if(G){r=G(r);}e[j][r]=v;});}d.sort(function(a,b){if(G){a=G(a);b=G(b);}var f=e[0][a],h=e[0][b];return t._applySortCompare(s,a,b,f,h,e,C,0);});return d;};c._applySortCompare=function(s,a,b,v,d,e,C,D){var o=s[D],f=C[D],r;r=f(v,d);if(o.bDescending){r=-r;}if(r==0&&s[D+1]){v=e[D+1][a];d=e[D+1][b];r=this._applySortCompare(s,a,b,v,d,e,C,D+1);}return r;};return c;});
