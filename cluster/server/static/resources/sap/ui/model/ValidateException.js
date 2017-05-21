/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define(['sap/ui/base/Exception'],function(E){"use strict";var V=function(m,v){this.name="ValidateException";this.message=m;this.violatedConstraints=v;};V.prototype=Object.create(E.prototype);return V;},true);
