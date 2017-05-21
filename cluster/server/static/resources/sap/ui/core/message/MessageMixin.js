/*!
 * UI development toolkit for HTML5 (OpenUI5)
 * (c) Copyright 2009-2017 SAP SE or an SAP affiliate company.
 * Licensed under the Apache License, Version 2.0 - see LICENSE.txt.
 */
sap.ui.define([],function(){"use strict";var M=function(){this.refreshDataState=r;};function r(n,d){if(d.getChanges().messages){var m=d.getMessages();var l=sap.ui.core.LabelEnablement.getReferencingLabels(this);if(l&&l.length>0){var L=l[0];m.forEach(function(a){var b=sap.ui.getCore().byId(L);if(b.getMetadata().isInstanceOf("sap.ui.core.Label")&&b.getText){a.setAdditionalText(b.getText());}else{jQuery.sap.log.warning("sap.ui.core.message.Message: Can't create labelText."+"Label with id "+L+" is no valid sap.ui.core.Label.",this);}}.bind(this));}var o=sap.ui.getCore().getMessageManager().getMessageModel();o.checkUpdate();if(m&&m.length>0){var a=m[0];if(sap.ui.core.ValueState[a.type]){this.setValueState(a.type);this.setValueStateText(a.message);}}else{this.setValueState(sap.ui.core.ValueState.None);this.setValueStateText('');}}}return M;},true);
