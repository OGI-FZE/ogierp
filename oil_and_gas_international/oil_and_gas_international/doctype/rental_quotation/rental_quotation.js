// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Quotation', {
	before_submit: function (frm, cdt, cdn) {
		frappe.model.set_value(cdt, cdn, 'status', 'Open')
	},
	refresh(frm) {
		create_custom_buttons(frm)
	}
});

// Rental Quotation Item
frappe.ui.form.on('Rental Quotation Item', {
	quantity(frm, cdt, cdn) {
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
		add_rental_estimation()
	} else if (status == 1) {
		add_rental_order()
	}
}


const add_rental_estimation = () => {
	cur_frm.add_custom_button('Rental Estimation', () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: "Rental Estimation",
			target: this.cur_frm,
			setters: {
				status: ["in", ["Draft", "Pending Estimation"]],
			},
			date_field: "date",
			get_query() {
				return {
					filters: {}
				}
			},
			action(selections) {
				if (selections.length > 1) {
					frappe.msgprint("Please select only single Rental Estimation for importing items.")
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
								'asset_location': row.asset_location
							})
							const cdt = new_row.doctype
							const cdn = new_row.name
							frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
						}

						cur_frm.refresh()
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
				cur_doc.date = doc.date
				cur_doc.rental_quotation = doc.name

				cur_doc.items = []
				for (const row of doc.items) {
					const new_row = cur_frm.add_child('items', {
						'qty': row.qty,
						'rate': row.rate,
						'location': row.asset_location,
						'rental_estimate': doc.name,
						'rental_estimate_item': row.name,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
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
const calc_amount = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.qty && row.rate)
		frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate)
}