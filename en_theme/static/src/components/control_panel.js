odoo.define('en_theme.ControlPanel', function (require) {
"use strict";

const ControlPanel = require('web.ControlPanel');
const config = require('web.config');

const { useState } = owl.hooks;

if (!config.device.isMobile) {
    return;
}

ControlPanel.patch('en_theme.ControlPanel', T => {
	
    class ControlPanelPatch extends T {
        constructor() {
            super(...arguments);
            this.state = useState({
                showViewSwitcherButtons: false,
            });
            this.isMobile = true;
        }
        mounted() {
            super.mounted();
            this.onWindowClickEvent = this._onWindowClick.bind(this);
            window.addEventListener('click', this.onWindowClickEvent);
        }
        willUnmount() {
            super.willUnmount();
            window.removeEventListener('click', this.onWindowClickEvent);
        }
        _onWindowClick(event) {
            if (this.state.showViewSwitcherButtons && !event.target.closest('.o_cp_switch_buttons')) {
                this.state.showViewSwitcherButtons = false;
            }
        }
        _getCurrentViewIcon() {
        	const currentView = this.props.views.find((view) => { 
        		return view.type === this.env.view.type 
        	})
        	return currentView.icon;
        }
    }

    return ControlPanelPatch;
});

});
