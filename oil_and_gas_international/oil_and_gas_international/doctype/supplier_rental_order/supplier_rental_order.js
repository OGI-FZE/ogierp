// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Supplier Rental Order', {
	setup(frm) {
		set_query(frm)
	},
	refresh(frm) {
		create_custom_buttons(frm)
	}
});

const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 0) {
		get_items_from_supplier_rental_quotation()
	} else if (status == 1) {
		add_supplier_rental_timesheet()
	}
}

frappe.ui.form.on('Supplier Rental Order Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
	},

	from_date(frm, cdt, cdn) {
		calc_days_of_rent(frm, cdt, cdn)
	},

	to_date(frm, cdt, cdn) {
		calc_days_of_rent(frm, cdt, cdn)
	},

	qty(frm, cdt, cdn) {
		calc_total_qty(frm, cdt, cdn)
	},
});

const set_query = (frm) => {
	frm.fields_dict['items'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
		return {
			filters: [
				['item_type', '=', 'Rental']
			]
		}
	}
}

const get_items_from_supplier_rental_quotation = () => {
	const doctype = "Supplier Rental Quotation"
	cur_frm.add_custom_button(doctype, () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: doctype,
			target: this.cur_frm,
			setters: { supplier: cur_frm.doc.supplier, },
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
					method: "get_supplier_rental_quotation_items",
					args: {
						docname: selections[0]
					},
					async: false,
					callback(res) {
						const data = res.message
						const cur_doc = cur_frm.doc
						cur_doc.supplier = data.supplier
						cur_doc.supplier_rental_quotation = data.name

						cur_doc.items = []
						for (const row of data.rq_items) {
							let rate = row.rate
							if (data.rate_type == "Per Month") {
								rate = rate / 30
							}

							const new_row = cur_frm.add_child('items', {
								'rate': rate,
								'asset_location': row.asset_location,
								'supplier_rental_quotation': data.name,
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

const add_supplier_rental_timesheet = () => {
	cur_frm.add_custom_button('Supplier Rental Timesheet', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Supplier Rental Timesheet'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.supplier = doc.supplier
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "supplier_rental_order", doc.name)

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




const calc_days_of_rent = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.from_date && row.to_date) {
		const to_date = new Date(row.to_date)
		const from_date = new Date(row.from_date)
		const difference = Math.floor((to_date - from_date) / (1000 * 60 * 60 * 24) + 1)

		if (difference < 1) {
			frappe.msgprint("To Date can't be before From date!")
			frappe.model.set_value(cdt, cdn, 'days_of_rent', 0)
			return
		}
		frappe.model.set_value(cdt, cdn, 'days_of_rent', difference)
	}
}


