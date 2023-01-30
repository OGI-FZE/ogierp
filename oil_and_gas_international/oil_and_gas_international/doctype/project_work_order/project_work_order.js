// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Work Order', {
	warehouse(frm) {
		if (frm.doc.sales_order_items){
			frm.doc.sales_order_items.forEach(function(item){
				frappe.db.get_value("Bin",{'warehouse':frm.doc.warehouse,'item_code': item.item_code}, ["actual_qty"], (r) => {
					// cur_frm.set_value("customer", r.customer)
					if (!r.actual_qty){
						frappe.model.set_value(item.doctype,item.name,'qty_in_warehouse',0)
						var dif_qty = item.qty_in_warehouse - item.qty
						console.log(item.qty_in_warehouse - item.qty)
						frappe.model.set_value(item.doctype,item.name,'dif_qty',dif_qty)
					}
					else{
						frappe.model.set_value(item.doctype,item.name,'qty_in_warehouse',r.actual_qty)
						var dif_qty = item.qty_in_warehouse - item.qty
						console.log(item.qty_in_warehouse - item.qty)
						frappe.model.set_value(item.doctype,item.name,'dif_qty',dif_qty)
					}
				})
			})
		}
		if (frm.doc.rental_order_items){
			frm.doc.rental_order_items.forEach(function(item){
				frappe.db.get_value("Bin",{'warehouse':frm.doc.warehouse,'item_code': item.item_code}, ["actual_qty"], (r) => {
					// cur_frm.set_value("customer", r.customer)
					if (!r.actual_qty){
						frappe.model.set_value(item.doctype,item.name,'qty_in_warehouse',0)
						var dif_qty = item.qty_in_warehouse - item.qty
						console.log(item.qty_in_warehouse - item.qty)
						frappe.model.set_value(item.doctype,item.name,'dif_qty',dif_qty)
					}
					else{
						frappe.model.set_value(item.doctype,item.name,'qty_in_warehouse',r.actual_qty)
						var dif_qty = item.qty_in_warehouse - item.qty
						console.log(item.qty_in_warehouse - item.qty)
						frappe.model.set_value(item.doctype,item.name,'dif_qty',dif_qty)
					}
				})
			})
		}
	}
});
