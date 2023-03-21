// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt
frappe.ui.form.on('RO Project WO Items', {
	warehouse(frm,cdt,cdn) {
		var child = locals[cdt][cdn];
		frappe.db.get_value("Bin",{'warehouse':child.warehouse,'item_code': child.item_code}, ["actual_qty"], (r) => {
			if (!r.actual_qty){
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',0)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
			else{
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',r.actual_qty)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
		})
    },
	
	qty(frm,cdt,cdn) {
		var child = locals[cdt][cdn];
		frappe.db.get_value("Bin",{'warehouse':child.warehouse,'item_code': child.item_code}, ["actual_qty"], (r) => {
			if (!r.actual_qty){
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',0)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
			else{
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',r.actual_qty)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
		})
    },
});

frappe.ui.form.on('SO Project WO Items', {
	warehouse(frm,cdt,cdn) {
		var child = locals[cdt][cdn];
		frappe.db.get_value("Bin",{'warehouse':child.warehouse,'item_code': child.item_code}, ["actual_qty"], (r) => {
			if (!r.actual_qty){
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',0)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
			else{
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',r.actual_qty)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
		})
    },
	qty(frm,cdt,cdn) {
		var child = locals[cdt][cdn];
		frappe.db.get_value("Bin",{'warehouse':child.warehouse,'item_code': child.item_code}, ["actual_qty"], (r) => {
			if (!r.actual_qty){
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',0)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
			else{
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',r.actual_qty)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
		})
    },
});

frappe.ui.form.on('Project WO Items', {
	warehouse(frm,cdt,cdn) {
		var child = locals[cdt][cdn];
		frappe.db.get_value("Bin",{'warehouse':child.warehouse,'item_code': child.item_code}, ["actual_qty"], (r) => {
			if (!r.actual_qty){
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',0)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
			else{
				frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',r.actual_qty)
				frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
			}
		})
   },
   qty(frm,cdt,cdn) {
	var child = locals[cdt][cdn];
	frappe.db.get_value("Bin",{'warehouse':child.warehouse,'item_code': child.item_code}, ["actual_qty"], (r) => {
		if (!r.actual_qty){
			frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',0)
			frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
		}
		else{
			frappe.model.set_value(child.doctype,child.name,'qty_in_warehouse',r.actual_qty)
			frappe.model.set_value(child.doctype,child.name,'dif_qty',child.qty_in_warehouse - child.qty)
		}
	})
},
});


frappe.ui.form.on('Project Work Order', {

	for_returned_material(frm) {
		frm.doc.rental_order_items.forEach(function(child){
					if(r.message) {
						if (frm.doc.for_returned_material==1){
							frappe.model.set_value(child.doctype,child.name,'qty',child.returned_qty)
						}
					}

		})



	},
	refresh(frm) {
		if (frm.doc.docstatus == 1) {
			create_inspection(frm)
			add_material_request(frm)
			add_subrent_quotation(frm)
			add_subrent_order(frm)
		}
    },

	onload(frm) {

		frm.fields_dict['rental_order_items'].grid.get_field('bom').get_query =
		function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
				  'item': child.item_code,
				  'purpose': child.purpose
			}
			}
		}


		frm.fields_dict['sales_order_items'].grid.get_field('bom_').get_query =
		function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
				  'item': child.item_code,
				  'purpose': child.purpose
			}
			}
		}


		frm.fields_dict['project_work_order_items'].grid.get_field('bom').get_query =
		function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
				  'item': child.item_code,
				  'purpose': child.purpose
			}
			}
		}


    }
	
});

const create_inspection = (frm) => {
    frm.add_custom_button('Route Card', () => {
        const doc = frm.doc;
        frappe.run_serially([
			() => {
				const data = []
				if (doc.rental_order){
					let qty_to_inspect;
					for (const row of doc.rental_order_items){
						if (row.purpose == "Manufacturing"){
							qty_to_inspect = row.qty
						}
						else if (row.qty_in_warehouse > row.qty){
							qty_to_inspect = row.qty
						}
						else {
							qty_to_inspect = row.qty_in_warehouse
						}

						data.push({'item_code': row.item_code,
									'item_category': row.item_category,
									'warehouse': row.warehouse,
									'qty':qty_to_inspect,
									'project': doc.project_reference,
									'project_wo': doc.name,
									'sales_order': doc.sales_order,
									'rental_order': doc.rental_order,
									'purpose':row.purpose,
									'bom': row.bom,
									'work_in_progress_warehouse': row.work_in_progress_warehouse,
									'final_warehouse': row.final_warehouse
									})
								}
						}
				
				if (doc.sales_order){
					let qty_to_inspect;
					
					for (const row of doc.sales_order_items){
						if (row.purpose == "Manufacturing"){
							qty_to_inspect = row.qty
						}
						else if (row.qty_in_warehouse > row.qty){
							qty_to_inspect = row.qty
						}
						else {
							qty_to_inspect = row.qty_in_warehouse
						}
						data.push({'item_code': row.item_code,
									'item_category': row.item_category,
									'warehouse': row.warehouse,
									'qty': qty_to_inspect,
									'project': doc.project_reference,
									'project_wo': doc.name,
									'sales_order': doc.sales_order,
									'rental_order': doc.rental_order,
									'purpose': row.purpose,
									'for_external_inspection': row.for_customer_inspection,
									'bom':row.bom_,
									'work_in_progress_warehouse': row.work_in_progress_warehouse,
									'final_warehouse': row.final_warehouse
									})
								}
							}
				if (!doc.sales_order && !doc.rental_order){
					let qty_to_inspect;
					for (const row of doc.project_work_order_items){
						if (row.purpose == "Manufacturing"){
							qty_to_inspect = row.qty
						}
						else if (row.qty_in_warehouse > row.qty){
							qty_to_inspect = row.qty
						}
						else {
							qty_to_inspect = row.qty_in_warehouse
						}

						if (row.qty_in_warehouse > row.qty){
							qty_to_inspect = row.qty
						}
						else {
							qty_to_inspect = row.qty_in_warehouse
						}
						data.push({'item_code': row.item_code,
									'item_category': row.item_category,
									'warehouse': row.warehouse,
									'qty': qty_to_inspect,
									'project': doc.project_reference,
									'project_wo': doc.name,
									'sales_order': doc.sales_order,
									'rental_order': doc.rental_order,
									'purpose': row.purpose,
									'for_external_inspection': row.for_customer_inspection,
									'bom': row.bom,
									'work_in_progress_warehouse': row.work_in_progress_warehouse,
									'final_warehouse': row.final_warehouse
									
									})
								}
							}
					const fields =	[{
						label: 'Items',
						fieldtype: 'Table',
						fieldname: 'items_to_inspect',
						description: __('Select'),
						fields: [{fieldtype: 'Link',fieldname: 'item_code',label: __('Item code'),options:'Item',in_list_view: 1,
								get_status: () => {return 'Read'}},
								{fieldtype: 'Link',fieldname: 'bom',label: __('BOM'),options:'BOM',in_list_view: 0,reqd:1,},
								//get_query: () => {return {filters: {'inspection_bom': 1}}}}, 
								{fieldtype: 'Data',fieldname: 'item_category',label: __('Item category'),in_list_view: 1,
								get_status: () => {return 'Read'}},
								{fieldtype: 'Link',fieldname: 'warehouse',label: __('Warehouse'),options:'Warehouse',in_list_view: 0,
								get_status: () => {return 'Read'}},
								{fieldtype: 'Link',fieldname: 'project',label: __('Project'),options:'Project',in_list_view: 0,
								get_status: () => {return 'Read'}},
								{fieldtype: 'Column Break',fieldname: 'col_bre',label: __(''),in_list_view: 0,get_status: () => {return 'Read'}},
								{fieldtype: 'Float',fieldname: 'qty',label: __('Quantity'),in_list_view: 1,get_status: () => {return 'Read'}},
								{fieldtype: 'Link',fieldname: 'project_wo',label: __('Project WO'),options:'Project Work Order',in_list_view: 0,
								get_status: () => {return 'Read'}},
								{fieldtype: 'Link',fieldname: 'sales_order',label: __('Sales Order'),options:'Sales Order',in_list_view: 0,
								get_status: () => {return 'Read'}},
								{fieldtype: 'Link',fieldname: 'rental_order',label: __('Rental Order'),options:'Rental Order',in_list_view: 0,
								get_status: () => {return 'Read'}},
								{fieldtype: 'Data',fieldname: 'purpose',label: __('Purpose'),in_list_view: 1,
								get_status: () => {return 'Read'}},
								{fieldtype: 'Check',fieldname: 'for_external_inspection',label: __('External Inspection'),
								get_status: () => {return 'Read'}},
								{fieldtype: 'Link',fieldname: 'work_in_progress_warehouse',label: __('Work-In-Progress-Warehouse'),
								get_status: () => {return 'Read'}},
								{fieldtype: 'Link',fieldname: 'final_warehouse',label: __('Final Warehouse'),
								get_status: () => {return 'Read'}},
					],

						data: data,
						get_data: () => {
							return data
						}
					}]
					
					let table = new frappe.ui.Dialog({
						title: 'Select Items to Create Route Card',
						fields: fields,
						primary_action_label: 'Create Route Card',
						primary_action: function() {
							
							var selected = {items_to_inspect: table.fields_dict.items_to_inspect.grid.get_selected_children()};
							for (const idx of selected.items_to_inspect){
								frm.call({
									method: 'oil_and_gas_international.oil_and_gas_international.doctype.inspection.inspection.create_wo',
									args: {
										"item_code" : idx.item_code,
										"warehouse": idx.warehouse,
										"item_category": idx.item_category,
										"project": idx.project,
										"project_wo": idx.project_wo,
										"sales_o": idx.sales_order,
										"rental_o": idx.rental_order,
										"qty": idx.qty,
										"bom": idx.bom,
										"purpose": idx.purpose,
										"for_cu_ins": idx.for_external_inspection,
										"final_warehouse": idx.final_warehouse,
										"work_in_progress_warehouse": idx.work_in_progress_warehouse
									},
									freeze: true,
									callback: function(r) {
										if(r.message) {
												frappe.msgprint({
												title: __('Route Card created'),
												message: __('Route Card created for the item selected.'),
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


const add_material_request = () => {
	cur_frm.add_custom_button('Material Request', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Material Request'),
			() => {
				const cur_doc = cur_frm.doc
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.rental_order)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "department", doc.department)
				
				cur_doc.items = []
				for (const row of doc.rental_order_items) {
					if (row.purpose == "Sub rent"){
						const new_row = cur_frm.add_child("items", {
							qty:row.qty
						})
						const cdt = new_row.doctype
						const cdn = new_row.name
						frappe.model.set_value(cdt.doctype, cdn.name, "item_code", row.item_code)

					}


				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}


const add_subrent_quotation = () => {
	cur_frm.add_custom_button('Sub Rent Quotation', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Supplier Rental Quotation'),
			() => {
				const cur_doc = cur_frm.doc
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.rental_order)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "department", doc.department)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "division", doc.division)
				
				cur_doc.items = []
				for (const row of doc.rental_order_items) {
					if (row.purpose == "Sub rent"){
						const new_row = cur_frm.add_child("items", {
							qty:row.qty
						})
						const cdt = new_row.doctype
						const cdn = new_row.name
						frappe.model.set_value(cdt, cdn, "item_code", row.item_code)

					}


				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_subrent_order = () => {
	cur_frm.add_custom_button('Sub Rent Order', () => {
		const doc = cur_frm.doc
		cur_frm.call({
			method: 'oil_and_gas_international.overriding.check_subrent_order_existence',
			args: {
				"rental_order" : doc.rental_order,
			},
			freeze: true,
			callback: function(r) {
				if(r.message == "False") {
					frappe.run_serially([
						() => frappe.new_doc('Supplier Rental Order'),
						() => {
							const cur_doc = cur_frm.doc
							frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.rental_order)
							frappe.model.set_value(cur_doc.doctype, cur_doc.name, "department", doc.department)
							frappe.model.set_value(cur_doc.doctype, cur_doc.name, "division", doc.division)
							frappe.model.set_value(cur_doc.doctype, cur_doc.name, "project", doc.project_reference)
							
							cur_doc.items = []
							for (const row of doc.rental_order_items) {
								if (row.purpose == "Sub rent"){
									const new_row = cur_frm.add_child("items", {
										qty:row.qty
									})
									const cdt = new_row.doctype
									const cdn = new_row.name
									frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
			
								}
			
			
							}
			
							cur_frm.refresh()
						}
					])
				}
				else{
					frappe.throw(__("Sub Rental Order Already created"))
				}
			}
		});

	}, 'Create')
}

