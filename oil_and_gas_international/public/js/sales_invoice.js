frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        create_custom_buttons(frm)
    }
})


const create_custom_buttons = (frm) => {
    frm.add_custom_button("Fetch Rental Timesheet", () => {
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
                    method: "oil_and_gas_international.events.sales_invoice.get_timesheet",
                    args: {
                        rental_orders: selections
                    },
                    callback(r) {
                        const data = r.message
                        for (const row in data) {
                            frm.add_child("items", {
                                item_code: row.item_code,
                                qty: row.qty,
                                rate: row.rate,
                                rental_order: row.rental_order,
                                rental_order_item: row.rental_order_item,
                                rental_timesheet: row.parent,
                                rental_timesheet_item: row.name
                            })
                        }

                        frm.refresh_field("items")
                        cur_dialog.hide()
                    }
                })
            }
        });
    })
}