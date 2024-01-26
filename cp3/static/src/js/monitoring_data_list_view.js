odoo.define('cp3.monitoring_data_list_view', function (require) {
    "use strict";
    var ListController = require("web.ListController");
    var ListView = require("web.ListView");
    var viewRegistry = require('web.view_registry');
    var core = require('web.core');
    var QWeb = core.qweb;

    var MonitoringDataListController = ListController.extend({
        buttons_template: 'MonitoringData.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_button_export_monitoring': '_export_monitoring',
        }),
        _export_monitoring: function () {
            var self = this;
            var action = {
                type: 'ir.actions.act_window',
                res_model: 'monitoring.data.wizard',
                view_mode: 'form',
                view_type: 'form',
                target: 'new',
                name: 'Export',
                views: [[false, 'form']],
            };
            var options = {
                on_close: function () {
                    self.trigger_up('reload');
                },
            };
            self.do_action(action, options)
        }
    });


    var ListViewMonitoringData = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: MonitoringDataListController
        }),
    });
    viewRegistry.add('monitoring_data_list_view', ListViewMonitoringData);
    return ListViewMonitoringData
});