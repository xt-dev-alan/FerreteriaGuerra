odoo.define('pos_prevent_access.pos', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');

    // Load the employee level fields
    models.load_fields("hr.employee", ["pos_discount_access", "pos_price_access", "pos_negative_access"]);

    // Load the user level fields
    models.load_fields("res.users", ["pos_discount_access", "pos_price_access", "pos_negative_access"]);

    // Load the option to check the access level
    models.load_models([{
        model:  'ir.config_parameter',
        fields: ['key', 'value'],
        domain: function(self){ return [['key', '=', "pos_prevent_access.pos_access_level"]]; },
        loaded: function(self, access) {
            if (access.length > 0) {
                var pos_access_user_level = access[0];
                if (pos_access_user_level.value == "True") {
                    self.pos_access_user_level = true;
                } else {
                    self.pos_access_user_level = false;
                }
            } else {
                self.pos_access_user_level = false;
            }
        }
    }]);

	screens.NumpadWidget.include({
        applyAccessRights: function() {
            // Stop the pos from using its own price control access by forcing it.
            // this._super();
            var cashier = this.pos.get('cashier') || this.pos.get_cashier();
            if (!this.pos.pos_access_user_level) {
                // Employee Level
                if (cashier.pos_discount_access == false) {
                    this.$el.find('.mode-button[data-mode="discount"]')
                    .toggleClass('disabled-mode', true)
                    .prop('disabled', true);
                    if (this.state.get('mode')=='discount') {
                        this.state.changeMode('quantity');
                    }
                } else {
                    this.$el.find('.mode-button[data-mode="discount"]')
                    .toggleClass('disabled-mode', false)
                    .prop('disabled', false);
                }
                if (cashier.pos_price_access == false) {
                    this.$el.find('.mode-button[data-mode="price"]')
                    .toggleClass('disabled-mode', true)
                    .prop('disabled', true);
                    if (this.state.get('mode')=='price') {
                        this.state.changeMode('quantity');
                    }
                } else {
                    this.$el.find('.mode-button[data-mode="price"]')
                    .toggleClass('disabled-mode', false)
                    .prop('disabled', false);
                }
                if (cashier.pos_negative_access == false) {
                    this.$el.find('.numpad-minus')
                    .toggleClass('disabled-mode', true)
                    .prop('disabled', true);
                    this.state.positiveSign();
                } else {
                    this.$el.find('.numpad-minus')
                    .toggleClass('disabled-mode', false)
                    .prop('disabled', false);
                }
            } else {
                // User Level
                var user = this.pos.user;
                if (user.pos_discount_access == false) {
                    this.$el.find('.mode-button[data-mode="discount"]')
                    .toggleClass('disabled-mode', true)
                    .prop('disabled', true);
                    if (this.state.get('mode')=='discount') {
                        this.state.changeMode('quantity');
                    }
                } else {
                    this.$el.find('.mode-button[data-mode="discount"]')
                    .toggleClass('disabled-mode', false)
                    .prop('disabled', false);
                }
                if (user.pos_price_access == false) {
                    this.$el.find('.mode-button[data-mode="price"]')
                    .toggleClass('disabled-mode', true)
                    .prop('disabled', true);
                    if (this.state.get('mode')=='price') {
                        this.state.changeMode('quantity');
                    }
                } else {
                    this.$el.find('.mode-button[data-mode="price"]')
                    .toggleClass('disabled-mode', false)
                    .prop('disabled', false);
                }
                if (user.pos_negative_access == false) {
                    this.$el.find('.numpad-minus')
                    .toggleClass('disabled-mode', true)
                    .prop('disabled', true);
                    this.state.positiveSign();
                } else {
                    this.$el.find('.numpad-minus')
                    .toggleClass('disabled-mode', false)
                    .prop('disabled', false);
                }

            }
        },
	});

});
