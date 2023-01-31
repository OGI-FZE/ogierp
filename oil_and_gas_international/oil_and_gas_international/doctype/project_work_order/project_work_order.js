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
			() => {
				const data = []
				if (doc.rental_order){
				for (const row of doc.rental_order_items){

					data.push({'item_code': row.item_code,
								'item_category': row.item_category,
								'warehouse': doc.warehouse,
								'qty':row.qty_in_warehouse,
								'project': doc.project_reference,
								'project_wo': doc.name,
								'sales_order': doc.sales_order,
								'rental_order': doc.rental_order,
								})
							}
						}
				
				if (doc.sales_order){
				for (const row of doc.sales_order_items){

					data.push({'item_code': row.item_code,
								'item_category': row.item_category,
								'warehouse': doc.warehouse,
								'qty':row.qty_in_warehouse,
								'project': doc.project_reference,
								'project_wo': doc.name,
								'sales_order': doc.sales_order,
								'rental_order': doc.rental_order,
								})
							}
						}
					const fields =	[{
						label: 'Items to inspect',
						fieldtype: 'Table',
						fieldname: 'items_to_inspect',
						description: __('Select'),
						fields: [{fieldtype: 'Link',fieldname: 'item_code',label: __('Item code'),options:'Item',in_list_view: 1}, 
								{fieldtype: 'Data',fieldname: 'item_category',label: __('Item category'),in_list_view: 1},
								{fieldtype: 'Link',fieldname: 'warehouse',label: __('Warehouse'),options:'Warehouse',in_list_view: 1},
								{fieldtype: 'Link',fieldname: 'project',label: __('Project'),options:'Project',in_list_view: 0},
								{fieldtype: 'Column Break',fieldname: 'col_bre',label: __(''),in_list_view: 0},
								{fieldtype: 'Float',fieldname: 'qty',label: __('Quantity'),in_list_view: 1,read_only:1},
								{fieldtype: 'Link',fieldname: 'project_wo',label: __('Project WO'),options:'Project Work Order',in_list_view: 1},
								{fieldtype: 'Link',fieldname: 'sales_order',label: __('Sales Order'),options:'Sales Order',in_list_view: 0},
								{fieldtype: 'Link',fieldname: 'rental_order',label: __('Rental Order'),options:'Rental Order',in_list_view: 0},

					],

						data: data,
						get_data: () => {
							return data
						}
					}]
					console.log("____________")
					console.log(data.length)
					
					let table = new frappe.ui.Dialog({
						title: 'Select Items to Create WO Inspection',
						fields: fields,
						primary_action_label: 'Create Inspection',
						primary_action: function() {
							
							var selected = {items_to_inspect: table.fields_dict.items_to_inspect.grid.get_selected_children()};
							for (const idx of selected.items_to_inspect){
								frm.call({
									method: 'oil_and_gas_international.events.inspection.create_inspection',
									args: {
										"item_code" : idx.item_code,
										"warehouse": idx.warehouse,
										"item_category": idx.item_category,
										"project": idx.project,
										"project_wo": idx.project_wo,
										"sales_o": idx.sales_order,
										"rental_o": idx.rental_order,
										"qty": idx.qty 
									},
									freeze: true,
									callback: function(r) {
										if(r.message) {
												frappe.msgprint({
												title: __('Work Order Inspection created'),
												message: __('Work Order Inspection generated for the Item selected.'),
												indicator: 'green'
											});
										}
										table.hide();
									}
								});
						}
						}
					})
					table.show();
				
			}
        ])
    }, 'Create');
}


