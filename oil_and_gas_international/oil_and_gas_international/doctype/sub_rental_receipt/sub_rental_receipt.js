// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sub Rental Receipt', {
	sub_rental_order(frm, cdt, cdn) {
		get_items_from_sub_rental_order(frm, cdt, cdn)
		set_project(frm)
	},
	refresh:function(frm){
		if(frm.is_new()){
			frappe.model.set_value('Sub Rental Receipt',frm.doc.name,'status','Draft')
		}
		create_custom_buttons()
	},
	setup(frm,cdt,cdn) {
		frm.fields_dict['items'].grid.get_field('assets').get_query = function (doc, cdt, cdn) {
			const row = locals[cdt][cdn]
			return {
				filters: {
					rental_status: "Sub Rental Asset",
					item_code:row.item_code,
					docstatus:1
				}
			}
		}
	}
});

const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 1){
		add_work_order()
	}
}

const add_work_order = () => {
	cur_frm.add_custom_button('Work_Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Work_Order'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.party_type = "Supplier"
				cur_doc.party = doc.supplier
				cur_doc.party_name = doc.supplier_name
				cur_doc.date = doc.date
				cur_doc.sub_rental_receipt = doc.name
				cur_doc.job_number = doc.project
				cur_doc.departments = doc.departments
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "sub_rental_order", doc.sub_rental_order)
				cur_frm.doc.items = []
				for (let row of doc.items) {
					cur_frm.add_child('items', {
						'quantity': row.qty,
						'item_code': row.item_code,
						'item_name': row.item_name,
						'assets': row.assets,
					})
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const get_items_from_sub_rental_order = (frm, cdt, cdn) => {
	const sub_rental_order = frm.doc.sub_rental_order
	frm.call({
		method: "get_sub_rental_order_items",
		args: { docname: sub_rental_order },
		async: false,
		callback(res) {
			const data = res.message
			if (!data) return
			frm.doc.items = []
			for (const row of data) {
				const new_row = frm.add_child('items', {
					'qty': row.qty,
					'rate': row.rate,
					'item_name': row.item_name,
					'asset_location': row.asset_location,
					'sub_rental_order': sub_rental_order,
					'sub_rental_order_item': row.name,
					'sub_rental_issue_note': frm.doc.sub_rental_issue_note || '',
				})

				const cdt = new_row.doctype
				const cdn = new_row.name
				frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
			}

			cur_frm.refresh()
		}
	})
}

frappe.ui.form.on('Sub Rental Receipt Item', {
	get_assets(frm, cdt, cdn) {
		get_assets_to_receive(frm, cdt, cdn)
	}
});

const set_project = (frm) => {
	const rental_order = frm.doc.sub_rental_order
	frappe.call({
		method: "oil_and_gas_international.tasks.get_project",
		args: { docname: rental_order },
		async: false,
		callback(res){
			const data = res.message
			frm.set_value("project", data.name)
		}
	})
}

const get_assets_to_receive = (frm, cdt, cdn) => {
	const doctype = "Asset"
	const row = locals[cdt][cdn]
	console.log("row",row.item_code);
	new frappe.ui.form.MultiSelectDialog({
		doctype: doctype,
		target: this.cur_frm,
		setters: {
			asset_name: null,
		},
		date_field: "transaction_date",

		get_query() {
			return {
				"filters": {
					"rental_status": "Sub Rental Asset",
					"item_code":row.item_code,
					"docstatus":1
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

