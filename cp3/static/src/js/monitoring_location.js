odoo.define('cp3.monitoring_location', function (require) {
    "use strict";
    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');
    var registry = require('web.field_registry');
    var core = require('web.core');
    var QWeb = core.qweb;

    // widget implementation
    var BoldWidget = basic_fields.FieldChar.extend({
        _renderReadonly: function () {
            this._super();
            var old_html_render = this.$el.html();
            var location_iframe = `<div>Not Find Location</div>`
            if (this.value !== '0,0') {
                location_iframe = QWeb.render('cp3.location_templates', {
                    location: this.value
                })
            }
            this.$el.html(location_iframe);
        },
    });

    registry.add('monitoring_location', BoldWidget); // add our "bold" widget to the widget registry
});