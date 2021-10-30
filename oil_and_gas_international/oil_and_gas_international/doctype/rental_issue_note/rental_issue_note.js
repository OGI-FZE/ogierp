// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Issue Note', {
	rental_order(frm, cdt, cdn) {
		get_items_from_rental_order(frm, cdt, cdn)
	}
});

frappe.ui.form.on('Rental Issue Note Item', {
	get_assets(frm, cdt, cdn) {
		get_assets_to_issue(frm, cdt, cdn)
	}
});


const get_items_from_rental_order = (frm, cdt, cdn) => {
	const rental_order = frm.doc.rental_order
	frm.call({
		method: "get_rental_order_items",
		args: { docname: rental_order },
		async: false,
		callback(res) {
			const data = res.message
			if (!data) return
			frm.doc.items = []
			for (const row of data) {
				
				const new_row = frm.add_child('items', {
					'qty': row.qty,
					'rate': row.rate,
					'asset_location': row.asset_location,
					'rental_order_item': row.name,
					'rental_order': row.parent,
				})

				const cdt = new_row.doctype
				const cdn = new_row.name
				frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
			}

			cur_frm.refresh()
		}
	})
}

const get_assets_to_issue = (frm, cdt, cdn) => {
	const doctype = "Asset"
	new frappe.ui.form.MultiSelectDialog({
		doctype: doctype,
		target: this.cur_frm,
		setters: {
			asset_name: null
		},
		date_field: "transaction_date",
		get_query() {
			return {
				filters: {
					rental_status: "Available For Rent",
				}
			}
		},
		action(selections) {
			const cur_row = locals[cdt][cdn]
			let serial_nos = ""
			for (const row of selections) {
				serial_nos += row + "\n"
			}

			cur_row.assets = serial_nos
			cur_frm.refresh()
			cur_dialog.hide()
		}
	});
}

