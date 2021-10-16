// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Order', {
	setup(frm) {
		set_query(frm)
	},

	refresh(frm) {
		create_custom_buttons(frm)
	}
});

// Rental Order Item
frappe.ui.form.on('Rental Order Item', {
	qty(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
		calc_total_qty(frm, cdt, cdn)
	},

	rate(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	amount(frm) {
		calc_total_amount(frm)
	},
});

// Rental Order
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
		get_items_from_rental_quotation()
	} else if (status == 1) {
		add_rental_order()
	}
}


const get_items_from_rental_quotation = () => {
	const doctype = "Rental Quotation"
	cur_frm.add_custom_button(doctype, () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: doctype,
			target: this.cur_frm,
			setters: { customer: cur_frm.doc.customer, },
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
					method: "get_rental_quotation_items",
					args: {
						docname: selections[0]
					},
					async: false,
					callback(res) {
						const data = res.message
						const cur_doc = cur_frm.doc
						cur_doc.customer = data.customer
						cur_doc.rental_quotation = data.name

						cur_doc.items = []
						for (const row of data.rq_items) {
							const new_row = cur_frm.add_child('items', {
								'rate': row.rate,
								'asset_location': row.asset_location
							})
							const cdt = new_row.doctype
							const cdn = new_row.name
							frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
							frappe.model.set_value(cdt, cdn, "qty", row.qty)
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
				cur_doc.date = doc.date
				cur_doc.rental_order = doc.name

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

const calc_total_qty = (frm) => {
	let total = 0
	frm.doc.items.map(row => {
		if (row.qty) total += row.qty
	})

	frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_qty', total)
}

const calc_total_amount = (frm) => {
	let total = 0
	frm.doc.items.map(row => {
		if (row.amount) total += row.amount
	})

	frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total', total)
}

// Rental Order Item
const calc_amount = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.qty && row.rate)
		frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate)
}