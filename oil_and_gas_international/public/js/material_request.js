frappe.ui.form.on("Material Request", {
    refresh(frm) {
        if (frm.doc.docstatus == 0) {
            create_custom_buttons(frm)
        }
        if (frm.doc.docstatus == 1){
            sub_rent_quotation(frm)

        }
    },

    // rental_order(frm) {
    //     const rental_order = frm.doc.rental_order

    //     frappe.call({
    //         method: "oil_and_gas_international.events.rental_order.get_rental_order_items",
    //         args: {
    //             docname: rental_order
    //         },
    //         async: false,
    //         callback(res) {
    //             const data = res.message
    //             cur_frm.doc.rental_order = data.name
    //             cur_frm.doc.items = []

    //             for (const row of data.ro_items) {
    //                 const new_row = cur_frm.add_child("items", {
    //                     qty: row.qty
    //                 })
    //                 const cdt = new_row.doctype
    //                 const cdn = new_row.name
    //                 frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
    //             }

    //             cur_frm.refresh()
    //         }
    //     })
    // }
})

const create_custom_buttons = (frm) => {
    get_items_from_rental_order(frm);
}

const get_items_from_rental_order = (frm) => {
    const doctype = "Rental Order"
    frm.add_custom_button(doctype, () => {
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

                const cdt = cur_frm.doc.doctype
                const cdn = cur_frm.doc.name
                frappe.model.set_value(cdt, cdn, "rental_order", selections[0])

                cur_dialog.hide()
            }
        });
    }, 'Get Items From');
}



const sub_rent_quotation = () => {
	cur_frm.add_custom_button('Sub Rental Quotation', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Supplier Rental Quotation'),
			() => {
                const cur_doc = cur_frm.doc
                cur_doc.rental_order = doc.rental_order
				cur_doc.items = []
				for (const row of doc.items) {
                    
					const new_row = cur_frm.add_child("items", {
						qty: row.qty,
						// serial_no_accepted: row.serial_no_accepted,

					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                    frappe.model.set_value(cdt,cdn,"description", row.description)
                    frappe.model.set_value(cdt,cdn,"uom", row.uom)
                    frappe.model.set_value(cdt, cdn, "item_name", row.item_name)

				}


				cur_frm.refresh()
				cur_frm.refresh()
			}
		])
	}, 'Create')
}