frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        create_custom_buttons(frm)
        
    },
    validate:function(frm){
        if(frm.doc.rental_order){
            frappe.db.get_doc('Rental Order',frm.doc.rental_order )
            .then(doc => {
                for(let row of doc.items){
                    for(let item of frm.doc.items){
                        if(row.item_code==item.asset_item){
                            const cdt=item.doctype;
                            const cdn=item.name;
                            frappe.model.set_value(cdt,cdn,'rate',row.total_amount)
                        }
                    }   
                }
            })
        }
    }
})



const create_custom_buttons = (frm) => {
    frm.add_custom_button("Fetch Rental Order", () => {
        if (!frm.doc.customer) {
            frappe.throw("Please select customer!")
        }

        const doctype = "Rental Order"
        new frappe.ui.form.MultiSelectDialog({
            doctype: doctype,
            target: this.cur_frm,
            setters: {},
            date_field: "date",
            get_query() {
                return {
                    filters: {
                        docstatus: 1,
                        customer: frm.doc.customer
                    }
                }
            },
            action(selections) {
                frappe.call({
                    method: "oil_and_gas_international.events.sales_invoice.get_rental_order_items",
                    args: {
                        rental_orders: selections
                    },
                    callback(r) {
                        frm.doc.items = []
                        const data = r.message
                        for (const row of data) {
                            const new_row = frm.add_child("items", {
                                "rental_order": row.rental_order,
                                "rental_order_item": row.rental_order_item,
                                "rental_timesheet": row.parent,
                                "rental_timesheet_item": row.name,
                            })

                            const cdt = new_row.doctype
                            const cdn = new_row.name
                            frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                            frappe.model.set_value(cdt, cdn, "qty", row.qty)
                            setTimeout(() => {
                                frappe.model.set_value(cdt, cdn, "rate", row.rate)
                            }, 1000);
                        }

                        frm.refresh_field("items")
                        cur_dialog.hide()
                    }
                })
            }
        });
    })
}