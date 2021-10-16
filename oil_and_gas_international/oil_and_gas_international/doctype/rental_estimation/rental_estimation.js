// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Estimation', {
	setup(frm) {
		set_query(frm)
	},
	refresh() {
		create_custom_buttons()
	}
})

frappe.ui.form.on('Rental Estimation Item', {
	qty(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	estimate_rate(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	amount(frm) {
		calc_total_amount(frm)
	},
})

// Rental Estimation
const set_query = (frm) => {
	frm.fields_dict['items'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
		return {
			filters: [
				['item_type', '=', 'Rental']
			]
		}
	}
}

const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 0) {
		get_items_from_opportunity()
	} else if (status == 1) {
		add_rental_quotation()
	}
}

const get_items_from_opportunity = () => {
	const doctype = "Opportunity"
	cur_frm.add_custom_button(doctype, () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: doctype,
			target: this.cur_frm,
			setters: {
				party_name: cur_frm.doc.customer,
			},
			date_field: "transaction_date",
			get_query() {
				return {
					filters: {
						opportunity_from: "Customer",
					}
				}
			},
			action(selections) {
				if (selections.length > 1) {
					frappe.msgprint(`Please select only single ${doctype} for importing items.`)
					return
				}
				cur_frm.call({
					method: "get_opportunity_items",
					args: {
						docname: selections[0]
					},
					async: false,
					callback(res) {
						const data = res.message
						cur_frm.doc.customer = data.party_name
						cur_frm.doc.opportunity = data.name
						cur_frm.doc.items = []

						for (const row of data.opportunity_items) {
							const new_row = cur_frm.add_child("items", {
								qty: row.qty
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

const add_rental_quotation = () => {
	cur_frm.add_custom_button('Rental Quotation', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Rental Quotation'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.date = doc.date
				cur_doc.valid_till = doc.valid_till
				cur_doc.rate_type = doc.rate_type
				cur_doc.rental_estimation = doc.name

				cur_doc.items = []
				for (const row of doc.items) {
					const new_row = cur_frm.add_child('items', {
						'qty': row.qty,
						'estimate_rate': row.estimate_rate,
						'asset_location': row.asset_location,
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

// Rental Estimation Item
const calc_amount = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.qty && row.estimate_rate)
		frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.estimate_rate)
}