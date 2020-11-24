odoo.define('pos_create_sales_order.pos', function(require) {
	"use strict";

	var models = require('point_of_sale.models');
	var screens = require('point_of_sale.screens');
	var core = require('web.core');
	var gui = require('point_of_sale.gui');
	var popups = require('point_of_sale.popups');
	var field_utils = require('web.field_utils');
	var rpc = require('web.rpc');
	var session = require('web.session');
	var time = require('web.time');
	var utils = require('web.utils');
	var _t = core._t;

	// Start CreateSalesOrderButtonWidget
	
	var CreateSalesOrderButtonWidget = screens.ActionButtonWidget.extend({
		template: 'CreateSalesOrderButtonWidget',
		
		renderElement: function(){
			var self = this;
			this._super();
		  
		  this.$el.click(function(){
				
				var order = self.pos.get('selectedOrder');

				var partner_id = false
				if (order.get_client() != null)
					partner_id = order.get_client().id;
				
				 // Popup Occurs when no Customer is selected...
					if (!partner_id) {
						self.gui.show_popup('error', {
							'title': _t('Unknown customer'),
							'body': _t('You cannot Create Sales Order. Select customer first.'),
						});
						return;
					}

				var orderlines = order.orderlines;
				var cashier_id = self.pos.get_cashier().user_id[0];
				// Popup Occurs when not a single product in orderline...
					if (orderlines.length === 0) {
						self.gui.show_popup('error', {
							'title': _t('Empty Order'),
							'body': _t('There must be at least one product in your order before Create Sales Order.'),
						});
						return;
					}
				
				var pos_product_list = [];
				for (var i = 0; i < orderlines.length; i++) {
					var product_items = {
						'id': orderlines.models[i].product.id,
						'quantity': orderlines.models[i].quantity,
						'uom_id': orderlines.models[i].product.uom_id[0],
						'price': orderlines.models[i].price,
						'discount': orderlines.models[i].discount,
					};
					
					pos_product_list.push({'product': product_items });
				}
				
				rpc.query({
					model: 'pos.create.sales.order',
					method: 'create_sales_order',
					args: [partner_id, partner_id, pos_product_list, cashier_id],
				
				}).then(function(output) {
					
					alert('Sales Order Created !!!!');  
					self.gui.show_screen('products');
					self.pos.delete_current_order();

				});

			});
			
		},
		
		button_click: function(){},
			highlight: function(highlight){
			this.$el.toggleClass('highlight',!!highlight);
		},
		
	});

	screens.define_action_button({
		'name': 'Create Sales Order Button Widget',
		'widget': CreateSalesOrderButtonWidget,
		'condition': function() {
			return true;
		},
	});
	// End CreateSalesOrderButtonWidget	


});
