odoo.define('cp3.monitoring_chartjs', function (require) {
    "use strict";
    var basic_fields = require('web.basic_fields');
    var registry = require('web.field_registry');
    var registry = require('web.field_registry');
    var core = require('web.core');
    var QWeb = core.qweb;

    var ChartJsWidget = basic_fields.FieldChar.extend({
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        events: _.extend({}, basic_fields.FieldChar.prototype.events, {
            'click .export_png': 'downloadImage',
        }),
        downloadImage: function (e) {
            e.stopPropagation();
            e.preventDefault();
           var link = document.createElement('a');
           link.href = this.mnChart.toBase64Image();
           link.download = this.data.name + '.png';
           link.click();
        },
         willStart: function () {
            var self = this
            var get_datas = this._rpc({
                model: 'monitoring.data',
                method: 'get_datas',
                args: [self.res_id],
            }).then(function (result) {
                self.data = result
            });
            return Promise.all([this._super.apply(this, arguments), get_datas]);
        },
        _renderReadonly: function () {
            var self = this
            this._super();
            setTimeout(()=> {
                if (self.data.dataset.length > 0) {
                    self.renderChart();
                }

            },500)

        },
        renderChart: function () {
            var data = {
                labels: this.data.key,
                datasets: [{
                        type: 'line',
                        label: this.data.name,
                        data: this.data.dataset.map(item=> item.toFixed(5)),
                        fill: false,
                        borderColor: '#0006ff',
                        tension: 0,
                        pointRadius: 3,
                        borderColor: "#0006ff",
                        pointBorderColor: "#0006ff",
                        pointBackgroundColor: "#0006ff",
                    },
                    {
                        type: 'line',
                        label: 'Warning',
                        data: this.data.warning,
                        fill: false,
                        borderColor: '#469207',
                        tension: 0,
                        pointRadius: 0
                    },
                    {
                        type: 'line',
                        label: 'Warning 1',
                        data: this.data.warning.map(item=> -1 * item),
                        fill: false,
                        borderColor: '#469207',
                        tension: 0,
                        pointRadius: 0,
                    },
                    {
                        type: 'line',
                        label: "Alarm",
                        data: this.data.alarm,
                        fill: false,
                        borderColor: '#c69305',
                        tension: 0,
                        pointRadius: 0
                    },
                    {
                        type: 'line',
                        label: "Alarm 1",
                        data: this.data.alarm.map(item=> -1 * item),
                        fill: false,
                        borderColor: '#c69305',
                        tension: 0,
                        pointRadius: 0
                    },
                    {
                        type: 'line',
                        label: "Alert",
                        data: this.data.alert,
                        fill: false,
                        borderColor: '#ec1818',
                        tension: 0,
                        pointRadius: 0
                    },
                    {
                        type: 'line',
                        label: "Alert 1",
                        data: this.data.alert.map(item=> -1 * item),
                        fill: false,
                        borderColor: '#ec1818',
                        tension: 0,
                        pointRadius: 0
                    }
                ]
            };
            $(this.__parentedParent.$el).find('.chartjs').removeClass('o_field_empty ');
            $(this.__parentedParent.$el).find('.chartjs').append(`
                <canvas id='chartjs' style="height:500px; width:100%;"/>
            `)
            $(this.__parentedParent.$el).find('.chartjs').prepend(QWeb.render('cp3.optional_chartjs', {}))
            let delayed;
            var ctx = document.getElementById("chartjs");
            this.mnChart = new Chart(ctx, {
                type: 'line',
                data: data,
                options: {
                    responsive: true,
                    legend: { display: false },
                    title:{
                        display:true,
                        text: this.data.name
                    },
                    tooltips: {
                        mode: 'index',
                        intersect: false,
                    },
                    hover: {
                        mode: 'nearest',
                        intersect: true
                    },
                    scales: {
                        xAxes: [{
                            barPercentage: 1,
                            stacked: true,
                            scaleLabel: {
                                display: true,
                              },
                            gridLines: {
                                display: true,
                                drawBorder: false,
                                tickMarkLength: false,
                                zeroLineColor:'transparent'
                            },
                            max: 5000
                        }],
                        yAxes: [{
                            barPercentage: 1,
                            scaleLabel: {
                                display: true,
                              },
                            stacked: true,
                            gridLines: {
                                display: true,
                            },

                        }]
                    },
                    animation: {
                        onComplete: () => {
                            delayed = true;
                        },
                        delay: (context) => {
                            let delay = 0;
                            console.log(context);
                            if (context.type === 'data' && context.mode === 'default' && !delayed) {
                                delay = context.dataIndex * 2000 + context.datasetIndex * 100;
                            }
                            return delay;
                        },
                    },
                }
            });
        }
    });

    registry.add('monitoring_chartjs', ChartJsWidget);
});