sap.ui.define(
    ["sap/ui/core/UIComponent",
        "sap/ui/model/json/JSONModel",
        "sap/ui/Device"
    ],
    function (UIComponent, JSONModel, Device) {
        "use strict";
        return UIComponent.extend("ch.berncon.generator.ui5.Component", {
            metadata: {
                manifest: "json"
            },
            init: function () {

                // set the device model
                this.setModel(new JSONModel(Device), "device");
                

                // call the base component's init function and create the App view
                UIComponent.prototype.init.apply(this, arguments);

                // call the init function of the parent
                UIComponent.prototype.init.apply(this, arguments);

                // create the views based on the url/hash
                this.getRouter().initialize();
            }
        });
    });
