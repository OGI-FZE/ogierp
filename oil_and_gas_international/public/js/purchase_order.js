frappe.ui.form.on("Purchase Order", {
    refresh(frm) {
        if (frm.doc.docstatus == 0) {
            create_custom_buttons(frm)
        }
    },
    rental_order(frm,cdt,cdn) {
        if(frm.doc.rental_order){
            set_project(frm,cdt,cdn)
        }
    },
})

const set_project = (frm,cdt,cdn) => {
    const rental_order = frm.doc.rental_order
    frappe.call({
        method: "oil_and_gas_international.oil_and_gas_international.doctype.rental_issue_note.rental_issue_note.get_project",
        args: { docname: rental_order },
        async: false,
        callback(res){
            const data = res.message
            frappe.model.set_value(cdt, cdn, "project",data.name)
        }
    })
}


const create_custom_buttons = (frm) => {
    get_items_from_rental_order(frm);
}

const get_items_from_rental_order = (frm) => {
    const doctype = "Rental Order"
    frm.add_custom_button(doctype, (frm) => {
        new frappe.ui.form.MultiSelectDialog({
            doctype: doctype,
            target: this.cur_frm,
            setters: {},
            date_field: "date",
            get_query() {
                return {
                    filters: {
                        status: "Draft",
                    }
                }
            },
            action(selections) {
                if (selections.length > 1) {
                    frappe.msgprint(`Please select only single ${doctype} for importing items.`)
                    return
                }
                cur_frm.call({
                    method: "oil_and_gas_international.events.rental_order.get_rental_order_items",
                    args: {
                        docname: selections[0]
                    },
                    async: false,
                    callback(res) {
                        const data = res.message
                        cur_frm.doc.rental_order = data.name
                        cur_frm.doc.items = []

                        for (const row of data.ro_items) {
                            const new_row = cur_frm.add_child("items", {
                                qty: row.qty
                            })
                            const cdt = new_row.doctype
                            const cdn = new_row.name
                            frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                        }

                        cur_frm.refresh()
                        cur_dialog.hide()
                    }
                })

            }
        });
    }, 'Get Items From');
}