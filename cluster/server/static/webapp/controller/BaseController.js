sap.ui.define(["sap/ui/core/mvc/Controller",
        "sap/ui/core/routing/History",
        'sap/m/Dialog'
    ],
    function (Controller, History, Dialog) {
        "use strict";
        return Controller.extend("ch.berncon.generator.ui5.BaseController", {

                getRouter: function () {
                    return sap.ui.core.UIComponent.getRouterFor(this);
                },

                onNavBack: function (oEvent) {
                    var oHistory = History.getInstance();
                    var sPreviousHash = oHistory.getPreviousHash();
                    if (sPreviousHash !== undefined) {
                        window.history.go(-1);
                    } else {
                        /* no history */
                        this.getRouter().navTo("main", {}, true);
                    }
                },

                getMessagePopoverInstance: function () {
                    if (!this.oMessagePopover) {
                        this.oMessagePopover = new sap.m.MessagePopover({
                            items: {
                                path: "message>/",
                                template: new sap.m.MessagePopoverItem({
                                    description: "{message>description}",
                                    type: "{message>type}",
                                    title: "{message>message}"
                                })
                            }
                        });
                        this.oMessagePopover.setModel(sap.ui.getCore().getMessageManager().getMessageModel(), "message");
                    }
                    return this.oMessagePopover;

                }

            }

        );

    });
