sap.ui.define(['ch/berncon/generator/ui5/controller/BaseController',
    'sap/ui/model/json/JSONModel',
    'ch/berncon/generator/ui5/model/formatter',
    'sap/ui/Device'
], function (BaseController, JSONModel,
    formatter, Device) {
    "use strict";
    return BaseController.extend('ch.berncon.generator.ui5.controller.Main', {
        formatter: formatter,

        onInit: function (oEvent) {
            var oRouter = this.getRouter();
            oRouter.getRoute("main").attachMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function (oEvent) {},


        onPress: function (oEvent) {
            var item = oEvent.getParameter('listItem');
           
             this.getRouter().navTo('newsDetail',{
                 id: item.getBindingContext('data').getPath().slice(1)
             });
        }
    });
});
