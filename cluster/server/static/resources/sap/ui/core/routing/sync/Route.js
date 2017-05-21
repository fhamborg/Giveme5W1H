/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['jquery.sap.global'],function(q){"use strict";return{_routeMatched:function(a,i,n){var r=this._oRouter,p,P,t,c,e,v=null,T=null,o;if(this._oParent){p=this._oParent._routeMatched(a);}else if(this._oNestingParent){this._oNestingParent._routeMatched(a,false,this);}c=q.extend({},r._oConfig,this._oConfig);o=q.extend({},a);o.routeConfig=c;e={name:c.name,arguments:a,config:c};if(n){e.nestedRoute=n;}this.fireBeforeMatched(e);r.fireBeforeRouteMatched(e);if(this._oTarget){t=this._oTarget;t._oOptions=this._convertToTargetOptions(c);if(t._isValid(p,false)){P=t._place(p);}P=P||{};v=P.oTargetParent;T=P.oTargetControl;e.view=v;e.targetControl=T;}else{r._oTargets._display(this._oConfig.target,o,this._oConfig.titleTarget);}if(c.callback){c.callback(this,a,c,T,v);}this.fireEvent("matched",e);r.fireRouteMatched(e);if(i){q.sap.log.info("The route named '"+c.name+"' did match with its pattern",this);this.fireEvent("patternMatched",e);r.fireRoutePatternMatched(e);}return P;}};});
