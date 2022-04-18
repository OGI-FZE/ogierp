// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Proforma Invoice', {
	refresh: function(frm) {
		if(frm.doc.docstatus==1){
			add_sales_invoice()
		}
		else{
			frm.trigger('calculate_amount');
		}
	},
    rental_timesheet(frm, cdt, cdn) {
        if(frm.doc.rental_timesheet){
		    get_items_from_rental_timesheet(frm, cdt, cdn)
        }
	},
	calculate_amount: function (frm){
		let doc = frm.doc;
		let total_qty = 0;
		let net_total = 0;
		for (let i in doc.items){
			total_qty += doc.items[i].qty;
			net_total += doc.items[i].amount;      
		}

		frm.refresh_field('items');
		frm.set_value('total_qty', total_qty);
		frm.set_value('net_total', net_total);
	}
});

frappe.ui.form.on('Proforma Invoice Item', {
	qty:function(frm,cdt,cdn){
		var d = locals[cdt][cdn]
		frappe.model.set_value(cdt, cdn, "net_total", d.amount)
		frm.trigger('calculate_amount');
	},

	rate:function(frm,cdt,cdn){
		var d = locals[cdt][cdn]
		frappe.model.set_value(cdt, cdn, "net_total", d.amount)
		frm.trigger('calculate_amount');
	}
});


const get_items_from_rental_timesheet = (frm, cdt, cdn) => {
	const rental_timesheet = frm.doc.rental_timesheet
	frappe.call({
		method: "oil_and_gas_international.events.sales_invoice.get_rental_timesheet_items",
		args: { docname: rental_timesheet },
		async: false,
		callback(res) {
			const data = res.message
			console.log(data)
			if (!data) return
			frm.doc.items = []
			for (const row of data) {
                const new_row = cur_frm.add_child("items", {
                    qty: 1,
                    asset_item:row.item_code,
                    rental_order:row.rental_order,
                    rental_order_item:row.rental_order_item,
                    days:row.days,
                    asset_qty:row.qty,
                    stock_qty:1
                })
                const cdt = new_row.doctype
                const cdn = new_row.name
                frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
                frappe.model.set_value(cdt, cdn, "item_name",'Asset Rent Item')
                frappe.model.set_value(cdt, cdn, "uom",'Nos')
                frappe.model.set_value(cdt, cdn, "stock_uom",'Nos')
                frappe.model.set_value(cdt, cdn, "conversion_factor",1)
                var item_name = ''
                var item_grp = ''
                let desc = ""
                if(row.item_code) {desc += row.item_name+"\n"}
                if(row.operational_running_days){
                	desc += "Operational/Running  " 
                	frappe.model.set_value(cdt, cdn, "unit_price",row.operational_running)
                }
                if(row.standby_days){
                	desc += "Standby  "
                	frappe.model.set_value(cdt, cdn, "unit_price",row.standby)
                }
                if(row.straight_days){
                	desc += "Straight  "
                	frappe.model.set_value(cdt, cdn, "unit_price",row.straight)
                }
                if(row.timesheet_start_date && row.timesheet_end_date) {desc += ("\nRental period: "+ row.timesheet_start_date +" to "+row.timesheet_end_date)}
                setTimeout(function(){
                    frappe.model.set_value(cdt, cdn, "price_list_rate",row.amount)
                    frappe.model.set_value(cdt, cdn, "rate",row.amount)
                    frappe.model.set_value(cdt, cdn, "amount",row.amount)
                    frappe.model.set_value(cdt, cdn, "net_rate",row.amount)
                    frappe.model.set_value(cdt, cdn, "net_amount",row.amount)
                    frappe.model.set_value(cdt, cdn, "details",desc)
                    frappe.model.set_value(cdt, cdn, "child_category",row.item_group)
                    frappe.model.set_value(cdt, cdn, "description",desc)
                }, 2000);           
				
			}

			cur_frm.refresh()
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
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_timesheet", doc.rental_timesheet)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "currency", doc.currency)
				cur_doc.items = []
				console.log("itemss",doc.items)
				for (const row of doc.items) {
					console.log("qty",row.qty)
					const new_row = cur_frm.add_child("items", {
						qty: row.qty,
						asset_item:row.item_code,
						rental_order:row.rental_order,
						rental_order_item:row.rental_order_item,
						assets:row.assets,
						item_code:row.item_code,
						item_name:row.item_name
					})
					console.log("new_row",new_row)
					const cdt = new_row.doctype
					const cdn = new_row.name
					// frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
					// frappe.model.set_value(cdt, cdn, "item_name",'Asset Rent Item')
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