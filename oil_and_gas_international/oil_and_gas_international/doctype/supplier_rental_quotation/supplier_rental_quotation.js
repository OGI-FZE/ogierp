// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Supplier Rental Quotation', {
	setup: function (frm) {
		frm.set_query("item_code", "items", function(doc, cdt, cdn) {
			return {
				filters: {
					is_fixed_asset: 1,
				}
			}
		})
	},
	refresh(frm) {
		create_custom_buttons(frm)
	}
});

const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 1) {
		add_supplier_rental_order()
	}
}

const add_supplier_rental_order = () => {
	cur_frm.add_custom_button('Supplier Rental Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Supplier Rental Order'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.supplier = doc.supplier
				cur_doc.supplier_rental_quotation = doc.name

				cur_doc.items = []
				for (const row of doc.items) {
					let rate = row.rate
					if (doc.rate_type == "Per Month") {
						rate = rate / 30
					}

					const new_row = cur_frm.add_child('items', {
						'rate': rate,
						'asset_location': row.asset_location,
						'supplier_rental_quotation': doc.name,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
					setTimeout(function() {
						frappe.model.set_value(cdt, cdn, "qty", row.qty)
						frappe.model.set_value(cdt, cdn, "operational_running", row.operational_running)
						frappe.model.set_value(cdt, cdn, "lihdbr", row.lihdbr)
						frappe.model.set_value(cdt, cdn, "standby", row.standby)
						frappe.model.set_value(cdt, cdn, "redress", row.redress)
						frappe.model.set_value(cdt, cdn, "straight", row.straight)
					}, 2000);
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}



frappe.ui.form.on('Supplier Rental Quotation Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
	},
	qty(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	rate(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	amount(frm) {
		calc_total_amount(frm)
	},
});

const calc_total_amount = (frm) => {
	let total = 0
	frm.doc.items.map(row => {
		if (row.amount) total += row.amount
	})

	frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total', total)
}

// Supplier Rental Quotation Item
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
			row.operational_running = data[0]
			row.standby = data[1]
			row.lihdbr = data[2]
			row.redress = data[3]
			row.straight = data[4]
			row.post_rental_inspection_charges = data[5]
			frm.refresh()
		}
	})
}


const calc_amount = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.qty && row.rate)
		frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate)
}
