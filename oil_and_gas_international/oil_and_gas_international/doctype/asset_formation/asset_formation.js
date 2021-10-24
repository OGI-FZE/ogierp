// Copyright (c) 2020, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Asset Formation', {
	setup: function(frm){
		frm.events.set_item_queries(frm);
	},

	refresh: function (frm){
		frappe.breadcrumbs.add('Assets', 'Asset Formation')
		frm.events.set_item_queries(frm);
		frm.events.show_create_asset_button(frm);
	},

	item_code: function(frm) {
		frm.doc.items = []
		frm.refresh_field('items');
	},

	warehouse: function(frm) {
		frm.doc.items = []
		frm.refresh_field('items');
	},

	fetch_serial_no: function (frm) {
		frm.events.show_serial_dialog(frm);
	},

	show_create_asset_button: function (frm) {
		if (frm.doc.docstatus == 1 && frm.doc.status == 'Submitted'){
			frm.add_custom_button('Convert to Assets', () => {
				frm.call('create_assets')
				.then(r => {
					frm.reload_doc();
					frappe.msgprint('Asset Created in Draft Mode')
				})
			})
		}
	},

	set_item_queries: function(frm){
		// Stock Item Query
		frm.set_query('item_code', () => {
			return {
				filters : {
					is_fixed_asset: 0,
					is_stock_item: 1,
					has_serial_no: 1
				}
			}
		})

		// Asset Item Query
		frm.set_query('asset_item_code', () => {
			return {
				filters : {
					is_fixed_asset: 1
				}
			}
		})
	},

	show_serial_dialog: function (frm) {
		if (frm.doc.item_code && frm.doc.warehouse){
			new frappe.ui.form.MultiSelectDialog({
				doctype: "Serial No",
				target: frm,
				setters: {
					item_code: frm.doc.item_code,
				},
				date_field: "purchase_date",
				get_query() {
					return {
						filters: { 
							docstatus: ['!=', 2],
							status: 'Active',
							company: frm.doc.company,
							warehouse: frm.doc.warehouse
						}
					}
				},
				action(selections) {
					frm.doc.items = [];
					for (let i in selections) {
						frm.add_child('items', {
							item_code: frm.doc.item_code,
							serial_no: selections[i]
						});
					}
					frm.refresh_field('items');
					cur_dialog.hide();
				}
			});
		}else{
			frappe.msgprint('Select Item and Warehouse');
		}
	}
});
