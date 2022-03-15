// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Issue Note', {
	refresh(frm) {
		if(frm.is_new()){
			frappe.model.set_value('Rental Issue Note',frm.doc.name,'status','Draft')
		}
		create_custom_buttons()
	},
	rental_order(frm, cdt, cdn) {
		get_items_from_rental_order(frm, cdt, cdn)
		set_project(frm)
	},
	setup(frm,cdt,cdn) {
		frm.fields_dict['items'].grid.get_field('assets').get_query = function (doc, cdt, cdn) {
			const row = locals[cdt][cdn]
			let asset_list = []
			let filters = {};

		    $.each(doc.items, function(_idx, val) {
				if (val.assets) asset_list.push(val.assets);
			});

			console.log("asset_list",asset_list);
			console.log("len",asset_list.length);

		    if(asset_list.length){
		    	filters['rental_status'] = "Available For Rent";
		    	filters['item_code'] = row.item_code;
		    	filters['docstatus'] = 1;
		    	filters['name'] = ['not in',asset_list];
		    }
		    else{
		    	filters['rental_status'] = "Available For Rent";
		    	filters['item_code'] = row.item_code;
		    	filters['docstatus'] = 1;
		    }
			return {
				filters: filters
			}
		}
	}
});

frappe.ui.form.on('Rental Issue Note Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
	},

	// get_assets(frm, cdt, cdn) {
	// 	get_assets_to_issue(frm, cdt, cdn)
	// }
});


const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 0){
		add_work_order()
	}

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

const add_work_order = () => {
	cur_frm.add_custom_button('Work_Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Work_Order'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.party_type = "Customer"
				cur_doc.party = doc.customer
				cur_doc.party_name = doc.customer_name
				cur_doc.date = doc.date
				cur_doc.rental_issue_note = doc.name
				cur_doc.job_number = doc.project
				cur_doc.departments = doc.departments
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.rental_order)
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


const set_project = (frm) => {
	const rental_order = frm.doc.rental_order
	frm.call({
		method: "get_project",
		args: { docname: rental_order },
		async: false,
		callback(res){
			const data = res.message
			frm.set_value("project", data.name)
		}
	})
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
				for(let i = 0; i < row.qty; i++){
					const new_row = frm.add_child("items", {
						'item_code': row.item_code,
						'qty': 1,
						'rate':row.rate,
						'operational_running':row.operational_running,
						'standby':row.standby,
						'lihdbr':row.lihdbr,
						'redress':row.redress,
						'straight':row.straight,
						'post_rental_inspection_charges':row.post_rental_inspection_charges,
						'asset_location':row.asset_location,
						'rental_order_item':row.name,
						'rental_order':row.rental_order
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
				}
				// const new_row = frm.add_child('items', {
				// 	'qty': row.qty,
				// 	'rate': row.rate,
				// 	'asset_location': row.asset_location,
				// 	'rental_order_item': row.name,
				// 	'rental_order': row.parent,
				// })

				
				// frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
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
					item_code: row.item_code,
					docstatus:1
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
