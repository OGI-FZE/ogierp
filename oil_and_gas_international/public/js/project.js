frappe.ui.form.on('Project', {
	refresh(frm) {
        if (!frm.is_new()) {
            create_project_work_order(frm)
			create_stock_entry(frm)
        }
    },
	after_save(frm){
		if(frm.doc.rental_order){
			frappe.db.set_value("Rental Order", frm.doc.rental_order, "project",frm.doc.name);
		}
	}

});


const create_project_work_order = (frm) => {
    frm.add_custom_button('Project Work Order', () => {
        const doc = frm.doc;
        frappe.run_serially([
            () => frappe.new_doc('Project Work Order'),
            () => {
				cur_frm.doc.startdate = doc.expected_start_date
				cur_frm.doc.enddate = doc.expected_end_date
				cur_frm.doc.rental_order = doc.rental_order;
                cur_frm.doc.sales_order = doc.sales_order;
                cur_frm.doc.project_reference = doc.name;
				cur_frm.doc.department = doc.department;
				cur_frm.doc.date = frappe.datetime.nowdate()
				if (doc.rental_order){
					const ro_items = []
					frappe.db.get_value("Rental Order", doc.sales_order, ["customer"], (r) => {
						cur_frm.set_value("customer", r.customer)
						console.log(r.customer)
					})
					frappe.call({
							method:'oil_and_gas_international.events.sales_order.fill_ro_items_table',
							args: {
									'rental_order': doc.rental_order,
								},
					
					callback: function(r) {
						cur_frm.doc.rental_order_items = [];
						for (let item of r.message){
							
							const cur_doc = cur_frm.doc
							const new_row = cur_frm.add_child('rental_order_items',{
								'item_name': item.item_name,
								'description': item.description,
								'description_2': item.description_2,
								'customer_requirement': item.customer_requirement,
								'qty':item.qty,
								'item_category': item.item_category,
								'returned_qty': item.returned_qty

							})
							const cdt = new_row.doctype
							const cdn = new_row.name
							frappe.model.set_value(cdt, cdn, "item_code",item.item_code )
							

						}
						cur_frm.refresh()

					}
			    });

				}
				if (doc.sales_order){
					frappe.db.get_value("Sales Order", doc.sales_order, ["customer"], (r) => {
						cur_frm.set_value("customer", r.customer)
						console.log(r.customer)
					})
					if (doc.for_external_inspection){
						frappe.call({
							method:'oil_and_gas_international.events.sales_order.get_stock_entry_data',
							args: {
									'sales_order': doc.sales_order,
								},
					
						callback: function(r) {
							console.log(r.message.length)
							cur_frm.doc.sales_order_items = [];
							for (let item of r.message){
								
								const cur_doc = cur_frm.doc
								
								const new_row = cur_frm.add_child('sales_order_items',{
									'item_name': item.item_name,
									'description': item.description,
									'delivery_date':item.delivery_date,
									'qty':item.qty,
									'item_category': item.item_category,
									'for_customer_inspection': item.for_customer_inspection,
									'stock_entry': item.stock_entry

									//'warehouse': item.warehouse
								})
								const cdt = new_row.doctype
								const cdn = new_row.name
								frappe.model.set_value(cdt, cdn, "item_code",item.item_code )
								frappe.model.set_value(cdt,cdn,'warehouse',item.warehouse)
								cur_frm.set_value("stock_entry",item.stock_entry)

								
	
							}
							cur_frm.refresh()
	
						}
					});
					}
					else{
					frappe.call({
						method:'oil_and_gas_international.events.sales_order.fill_so_items_table',
						args: {
								'sales_order': doc.sales_order,
							},
				
					callback: function(r) {
						console.log(r.message.length)
						cur_frm.doc.sales_order_items = [];
						for (let item of r.message){
							
							const cur_doc = cur_frm.doc
							
							const new_row = cur_frm.add_child('sales_order_items',{
								'item_name': item.item_name,
								'description': item.description,
								'description_2': item.description_2,
								'customer_requirement': item.customer_requirement,
								'delivery_date':item.delivery_date,
								'qty':item.qty,
								'item_category': item.item_category,

							})
							const cdt = new_row.doctype
							const cdn = new_row.name
							frappe.model.set_value(cdt, cdn, "item_code",item.item_code )
							

						}
						cur_frm.refresh()

					}
				});
			}



				}
            }
        ])
	
    }, 'Create');
}




const create_stock_entry = (frm) => {
    frm.add_custom_button('Stock Entry', () => {
        const doc = frm.doc;
		if (!doc.for_external_inspection){
			frappe.throw(__("You can not receive a Material against this Project"))
		}
		frappe.db.get_value("Stock Entry",{"sales_order":doc.sales_order}, ["name"], (r) => {
			// cur_frm.set_value("customer", r.customer)
			if (r.name){
				frappe.throw(_("You have already created a stock entry against this project"))
			}
		})
		
        frappe.run_serially([
            () => frappe.new_doc('Stock Entry'),
            () => {
				cur_frm.doc.project = doc.name;
				cur_frm.doc.sales_order = doc.sales_order;
				cur_frm.doc.stock_entry_type = "Material Receipt"
				cur_frm.refresh()
            }
        ])
    }, 'Create');
}