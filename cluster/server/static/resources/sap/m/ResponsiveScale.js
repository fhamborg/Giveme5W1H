/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global','./library','sap/ui/core/Element'],function(q,l,E){"use strict";var S=E.extend("sap.m.ResponsiveScale",{metadata:{interfaces:["sap.m.IScale"],library:"sap.m",properties:{tickmarksBetweenLabels:{type:"int",group:"Appearance",defaultValue:0}}}});S.prototype.calcNumTickmarks=function(s,f,t){var m=Math.floor(s/f);m=t&&(m>t)?this._runStepsOptimization(t,m):m;return Math.floor(m);};S.prototype._runStepsOptimization=function(t,m){var s=m/t;while((t>1)&&(s%1!==0)){t--;s=m/t;}return t;};S.prototype.calcTickmarksDistance=function(t,s,e,f){var a=Math.abs(s-e),m=Math.floor(a/f),i=Math.ceil(m/t);return s+(i*f);};S.prototype.getHiddenTickmarksLabels=function(s,t,o,L){var j,c,h=new Array(t),i=Math.ceil(1/(o/L)),C=function(p){return p<<1;};if(i===1){return h;}i--;i|=i>>1;i|=i>>2;i|=i>>4;i|=i>>8;i|=i>>16;i++;i=i>>1;j=C(i);while(i){c=i;while(c<((t/2)+j)){h[c]=true;h[t-c-1]=true;c+=j;}i=i>>1;j=C(i);}return h;};return S;},true);
