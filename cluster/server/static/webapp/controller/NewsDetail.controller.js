sap.ui.define(['ch/berncon/generator/ui5/controller/BaseController',
    'sap/ui/model/json/JSONModel',
    'ch/berncon/generator/ui5/model/formatter',
    'sap/ui/Device'
], function (BaseController, JSONModel,
    formatter, Device) {
    "use strict";
    return BaseController.extend('ch.berncon.generator.ui5.controller.NewsDetail', {
        formatter: formatter,

        onInit: function (oEvent) {
            var oRouter = this.getRouter();
            oRouter.getRoute("newsDetail").attachMatched(this._onRouteMatched, this);
        },

        _onRouteMatched: function (oEvent) {
            this.args = oEvent.getParameter('arguments');
           
            this.getView().bindElement('data>/'+ this.args.id + '/');
        },
        
        findingsToString: function(input){
            var string = "";
            for (var key in input) {
              if (input.hasOwnProperty(key)) {
                    string += '['+key.slice(4) + ',' + input[key] +']\n';
              }
            }
            return string;
        }
    });
});
