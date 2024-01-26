odoo.define('report_xlsx.client_action', function (require) {
'use strict';

var ClientAction = require('report.client_action');
var core = require('web.core');
var QWeb = core.qweb;
const framework = require('web.framework');

var ClientActionXlsx = ClientAction.include({
    start: function () {
        var self = this;
        var supper = this._super.apply(this, arguments);
        var report = 'report.client_action.ControlButtons';
        if(this.report_name == 'report_xlsx.xlsx_iframe'){
            report = 'report_xlsx.client_action.ControlButtons';
        }
        this.$buttons = $(QWeb.render(report, {}));
        this.$buttons.on('click', '.o_report_print', this.on_click_print);
        this.$buttons.on('click', '.o_report_refresh_xlsx', this.on_refresh_xlsx_iframe);
        this.$buttons.on('click', '.o_report_export_xlsx_iframe', this.on_export_xlsx_iframe);
        this.controlPanelProps.cp_content = {
            $buttons: this.$buttons,
        };
        return supper
    },
    on_refresh_xlsx_iframe: function (e) {
        framework.blockUI();
        $('.o_report_iframe')[0].contentDocument.location.reload(true);
        $('iframe').on('load', function() {
            framework.unblockUI();
        })
    },
    on_export_xlsx_iframe: function (e) {
        const url = $('.o_report_iframe')[0].src;
        const options = new URL(url).searchParams.get('options');
        const ms_url = JSON.parse(decodeURIComponent(options)).ms_url;
        const decoded_ms_url = decodeURIComponent(ms_url);
        const download_url = decoded_ms_url.split('src=')[1];
        const link = document.createElement("a");
        link.href = download_url;
        link.download = 'Income_Expense.xlsx';
        link.click();
    },
});
});
