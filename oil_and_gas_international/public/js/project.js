frappe.ui.form.on('Project', {
	refresh(frm) {
        if (!frm.is_new()) {
            create_project_work_order(frm)
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
						console.log(r.message.length)
						cur_frm.doc.rental_order_items = [];
						for (let item of r.message){
							
							const cur_doc = cur_frm.doc
							
							const new_row = cur_frm.add_child('rental_order_items',{
								'item_name': item.item_name,
								'description': item.description,
								'description_2': item.description_2,
								'customer_requirement': item.customer_requirement,
								'qty':item.qty,
								'item_group': item.item_group,

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
								'item_group': item.item_group,

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
        ])
    }, 'Create');
}