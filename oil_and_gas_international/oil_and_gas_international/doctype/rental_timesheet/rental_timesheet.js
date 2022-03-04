// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Timesheet', {
	rental_order(frm, cdt, cdn) {
		get_items_from_rental_order(frm, cdt, cdn)
		set_project(frm)
	},
	refresh:function(frm){
		if(frm.is_new()){
			frappe.model.set_value('Rental Timesheet',frm.doc.name,'status','Draft')
		}
		else if(frm.doc.docstatus==1){
			add_sales_invoice()
			add_sales_order()
		}
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
				if (!row.on_hold) {
					frm.call({
						method: "check_issue_note",
						args: { docname: rental_order,itm: row.item_code },
						async: false,
						callback(rti) {
							const issuenote=rti.message
							if (issuenote){
								for(let r = 0; r < issuenote.length; r++){
									// for(let i = 0; i < row.qty; i++){
									const new_row = frm.add_child('items', {
										'qty': 1,
										'asset_location': row.asset_location,
										'rental_order': rental_order,
										'rental_order_item': row.name,
										'operational_running':row.operational_running,
										'standby':row.standby,
										'lihdbr':row.lihdbr,
										'redress':row.redress,
										'straight':row.straight,
										'assets':issuenote[r].assets,
									})
									const cdt = new_row.doctype
									const cdn = new_row.name
									frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
									// }
								}
							}
						}
					})
				}
			}

			cur_frm.refresh()
		}
	})
}


frappe.ui.form.on('Rental Timesheet Item', {
	get_assets(frm, cdt, cdn) {
		get_assets_to_receive(frm, cdt, cdn)
	},
	qty(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.qty){
			calculate_amount(frm,cdt,cdn)
		}
	},
	operational_running_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.operational_running_days){
			calculate_amount(frm,cdt,cdn)
		}
	},
	standby_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
			if(row.standby_days){
				console.log('working');
				calculate_amount(frm,cdt,cdn)
			}
	},
	redress_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.redress_days){
			calculate_amount(frm,cdt,cdn)
		}
	},
	lihdbr_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.lihdbr_days){
			calculate_amount(frm,cdt,cdn)
		}
	},
	straight_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.straight_days){
			calculate_amount(frm,cdt,cdn)
		}
	},
	operational_running(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.operational_running){
			calculate_amount(frm,cdt,cdn)
		}
	},
	standby(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.standby){
			calculate_amount(frm,cdt,cdn)
		}
	},
	redress(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.redress){
			calculate_amount(frm,cdt,cdn)
		}
	},
	lihdbr(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.lihdbr){
			calculate_amount(frm,cdt,cdn)
		}
	},
	straight(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.straight){
			calculate_amount(frm,cdt,cdn)
		}
	},
	post_rental_inspection_charges(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.post_rental_inspection_charges){
			calculate_amount(frm,cdt,cdn)
		}
	}
});

const calculate_amount=(frm,cdt,cdn)=>{
	let row= locals[cdt][cdn]
	let total=0
	if(row.operational_running_days && row.operational_running>0){
		total = row.operational_running_days*row.operational_running
		console.log(total);
	}
	if(row.standby_days && row.standby>0){
		total = total +( row.standby_days*row.standby)
		console.log(total);
	}
	if(row.redress_days && row.redress>0){
		total = total+ (row.redress)
		console.log(total);
	}
	if(row.lihdbr_days && row.lihdbr>0){
		total = total+ (row.lihdbr)
		console.log(total);
	}
	if(row.straight_days && row.straight>0){
		total = total+ ( row.straight_days*row.straight)
		console.log(total);
	}
	if(row.post_rental_inspection_charges >0){
		total = total+ ( row.post_rental_inspection_charges)
		console.log(total);
	}
	frappe.model.set_value(cdt,cdn,'amount',total*row.qty)

}

const get_assets_to_receive = (frm, cdt, cdn) => {
	const doctype = "Asset"
	new frappe.ui.form.MultiSelectDialog({
		doctype: doctype,
		target: this.cur_frm,
		setters: {
			asset_name: null,
		},
		date_field: "transaction_date",
		get_query() {
			return {
				filters: {
					rental_status: "In Use",
					rental_order: frm.doc.rental_order
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

const set_project = (frm) => {
	const rental_order = frm.doc.rental_order
	frappe.call({
		method: "oil_and_gas_international.oil_and_gas_international.doctype.rental_issue_note.rental_issue_note.get_project",
		args: { docname: rental_order },
		async: false,
		callback(res){
			const data = res.message
			frm.set_value("project", data.name)
		}
	})
}

const add_sales_invoice = () => {
	cur_frm.add_custom_button('Sales Invoice', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Sales Invoice'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				// cur_doc.rental_timesheet = doc.name
				cur_doc.rental_order = doc.rental_order
				cur_doc.departments = doc.departments
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_timesheet", doc.name)
				cur_doc.items = []

				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						qty: 1,
						asset_item:row.item_code,
						rental_order:row.rental_order,
						rental_order_item:row.rental_order_item,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
					setTimeout(function(){
						frappe.model.set_value(cdt, cdn, "price_list_rate",row.amount)
						frappe.model.set_value(cdt, cdn, "rate",row.amount)
						frappe.model.set_value(cdt, cdn, "amount",row.amount)
					}, 2000);
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_sales_order = () => {
	cur_frm.add_custom_button('Sales Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Sales Order'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				// cur_doc.rental_timesheet = doc.name
				cur_doc.rental_order = doc.rental_order
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_timesheet", doc.name)
				cur_doc.items = []

				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						qty: 1,
						asset_item:row.item_code,
						rental_order:row.rental_order,
						rental_order_item:row.rental_order_item,
						assets:row.assets,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
					setTimeout(function(){
						frappe.model.set_value(cdt, cdn, "price_list_rate",row.amount)
						frappe.model.set_value(cdt, cdn, "rate",row.amount)
						frappe.model.set_value(cdt, cdn, "amount",row.amount)
					}, 2000);
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

