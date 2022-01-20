// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Quotation', {
	refresh(frm) {
		create_custom_buttons(frm)
	}
});

// Rental Quotation Item
frappe.ui.form.on('Rental Quotation Item', {
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

// Rental Quotation
const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 0) {
		get_items_from_rental_estimation()
	} else if (status == 1) {
		add_rental_order()
	}
}


const get_items_from_rental_estimation = () => {
	const doctype = "Rental Estimation"
	cur_frm.add_custom_button(doctype, () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: doctype,
			target: this.cur_frm,
			setters: {
				status: ["in", ["Draft", "Pending Estimation"]],
				customer: cur_frm.doc.customer,
			},
			date_field: "date",
			get_query() {
				return {
					filters: {}
				}
			},
			action(selections) {
				if (selections.length > 1) {
					frappe.msgprint(`Please select only single ${doctype} for importing items.`)
					return
				}
				cur_frm.call({
					method: "get_rental_estimation_items",
					args: {
						docname: selections[0]
					},
					async: false,
					callback(res) {
						const data = res.message
						const cur_doc = cur_frm.doc
						cur_doc.customer = data.customer
						cur_doc.date = data.date
						cur_doc.valid_till = data.valid_till
						cur_doc.rate_type = data.rate_type
						cur_doc.rental_estimation = data.name

						cur_doc.items = []
						for (const row of data.re_items) {
							const new_row = cur_frm.add_child('items', {
								'qty': row.qty,
								'estimate_rate': row.estimate_rate,
								'asset_location': row.asset_location,
								'rental_estimate': data.name,
								'rental_estimate_item': row.name,
							})
							const cdt = new_row.doctype
							const cdn = new_row.name
							frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
						}

						cur_frm.refresh()
						cur_dialog.hide()
					}
				})

			}
		});
	}, 'Get Items From')
}

const add_rental_order = () => {
	cur_frm.add_custom_button('Rental Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Rental Order'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.rental_quotation = doc.name

				cur_doc.items = []
				for (const row of doc.items) {
					let rate = row.rate
					if (doc.rate_type == "Per Month") {
						rate = rate / 30
					}

					const new_row = cur_frm.add_child('items', {
						'rate': rate,
						'asset_location': row.asset_location,
						'rental_quotation': doc.name,
						'rental_estimation': row.rental_estimate,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
					frappe.model.set_value(cdt, cdn, "qty", row.qty)
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const calc_total_amount = (frm) => {
	let total = 0
	frm.doc.items.map(row => {
		if (row.amount) total += row.amount
	})

	frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total', total)
}

// Rental Quotation Item
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
			frm.refresh()
		}
	})
}


const calc_amount = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.qty && row.rate)
		frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate)
}