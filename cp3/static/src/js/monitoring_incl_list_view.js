odoo.define('cp3.monitoring_incl_list_view', function (require) {
    "use strict";
    var ListController = require("web.ListController");
    var ListView = require("web.ListView");
    var viewRegistry = require('web.view_registry');
    var core = require('web.core');
    var QWeb = core.qweb;

    var MonitoringInclListController = ListController.extend({
        buttons_template: 'MonitoringDataIncl.buttons',
        events: _.extend({}, ListController.prototype.events, {
            'click .o_button_convert_incl_monitoring': '_convert_incl_monitoring',
        }),
        _convert_incl_monitoring: function () {
            var self = this;
            var action = {
                type: 'ir.actions.act_window',
                res_model: 'monitoring.incl.convert.data.wizard',
                view_mode: 'form',
                view_type: 'form',
                target: 'new',
                name: 'Incl Convert',
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


    var ListViewMonitoringDataIncl = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: MonitoringInclListController
        }),
    });
    viewRegistry.add('monitoring_incl_list_view', ListViewMonitoringDataIncl);
    return ListViewMonitoringDataIncl
});