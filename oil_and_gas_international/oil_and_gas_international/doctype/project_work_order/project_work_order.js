// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Project Work Order', {
	refresh(frm) {
        if (!frm.is_new()) {
            create_inspection(frm)
        }
    },
	warehouse(frm) {
		if (frm.doc.sales_order_items){
			frm.doc.sales_order_items.forEach(function(item){
				frappe.db.get_value("Bin",{'warehouse':frm.doc.warehouse,'item_code': item.item_code}, ["actual_qty"], (r) => {
					if (!r.actual_qty){
						frappe.model.set_value(item.doctype,item.name,'qty_in_warehouse',0)
						frappe.model.set_value(item.doctype,item.name,'dif_qty',item.qty_in_warehouse - item.qty)
					}
					else{
						frappe.model.set_value(item.doctype,item.name,'qty_in_warehouse',r.actual_qty)
						frappe.model.set_value(item.doctype,item.name,'dif_qty',item.qty_in_warehouse - item.qty)
					}
				})
			})
		}
		if (frm.doc.rental_order_items){
			frm.doc.rental_order_items.forEach(function(item){
				frappe.db.get_value("Bin",{'warehouse':frm.doc.warehouse,'item_code': item.item_code}, ["actual_qty"], (r) => {
					if (!r.actual_qty){
						frappe.model.set_value(item.doctype,item.name,'qty_in_warehouse',0)
						frappe.model.set_value(item.doctype,item.name,'dif_qty',item.qty_in_warehouse - item.qty)
					}
					else{
						frappe.model.set_value(item.doctype,item.name,'qty_in_warehouse',r.actual_qty)
						frappe.model.set_value(item.doctype,item.name,'dif_qty',item.qty_in_warehouse - item.qty)
					}
				})
			})
		}
	}
});

const create_inspection = (frm) => {
    frm.add_custom_button('Inspection', () => {
        const doc = frm.doc;
        frappe.run_serially([
			frappe.throw(__("ddddddd"))
        ])
    }, 'Create');
}


