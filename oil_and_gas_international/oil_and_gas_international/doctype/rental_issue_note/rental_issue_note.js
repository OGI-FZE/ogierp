// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Issue Note', {
	refresh() {
		create_custom_buttons()
	},
	rental_order(frm, cdt, cdn) {
		get_items_from_rental_order(frm, cdt, cdn)
	}
});

frappe.ui.form.on('Rental Issue Note Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
	},

	get_assets(frm, cdt, cdn) {
		get_assets_to_issue(frm, cdt, cdn)
	}
});


const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 1) {
		add_rental_receipt()
	}
}


const add_rental_receipt = () => {
	cur_frm.add_custom_button('Rental Receipt', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Rental Receipt'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.rental_issue_note = doc.name
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.rental_order)

				cur_frm.refresh()
			}
		])
	}, 'Create')
}


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
	const row = locals[cdt][cdn]

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
					item_code: row.item_code
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

const calculate_lost_and_damage_price = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	const item_code = row.item_code

	frappe.call({
		method: "oil_and_gas_international.events.shared.get_lost_and_damage_prices",
		args: {
			item_code
		},
		callback(r) {
			const data = r.message
			row.lih_price = data[0]
			row.dbr_price = data[1]
			frm.refresh()
		}
	})
}
