// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Timesheet', {
	rental_order(frm, cdt, cdn) {
		get_items_from_rental_order(frm, cdt, cdn)
	},
	refresh:function(frm){
		if(frm.is_new()){
			frappe.model.set_value('Rental Timesheet',frm.doc.name,'status','Draft')
		}
		else if(frm.doc.docstatus==1){
			add_sales_invoice()
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
					const new_row = frm.add_child('items', {
						'qty': row.qty,
						'asset_location': row.asset_location,
						'rental_order': rental_order,
						'rental_order_item': row.name,
						'operational_running':row.operational_running,
						'standby':row.standby,
						'lihdbr':row.lihdbr,
						'redress':row.redress,
						'straight':row.straight,
					})

					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
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
		total = total+ ( row.redress_days*row.redress)
		console.log(total);
	}
	if(row.lihdbr_days && row.lihdbr>0){
		total = total+ ( row.lihdbr_days*row.lihdbr)
		console.log(total);
	}
	if(row.straight_days && row.straight>0){
		total = total+ ( row.straight_days*row.straight)
		console.log(total);
	}
	frappe.model.set_value(cdt,cdn,'amount',total)

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

const add_sales_invoice = () => {
	cur_frm.add_custom_button('Sales Invoice', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Sales Invoice'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.rental_timesheet = doc.name
				cur_doc.rental_order = doc.rental_order
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

