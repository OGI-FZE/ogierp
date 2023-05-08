frappe.ui.form.on("Request for Quotation", {
    refresh(frm) {
        if (frm.doc.docstatus == 1) {
            make_supplier_rental_quotation(frm)
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

const make_supplier_rental_quotation = (frm) => {
    frm.add_custom_button('Sub Rental Qutotation', () => {
        var dialog = new frappe.ui.Dialog({
        title: __("Create Sub Rental Quotation"),
        fields: [
            {	"fieldtype": "Link",
                "label": __("Supplier"),
                "fieldname": "supplier",
                "options": 'Supplier',
                "reqd": 1,
                get_query: () => {
                    return {
                        filters: [
                            ["Supplier", "name", "in", frm.doc.suppliers.map((row) => {return row.supplier;})]
                        ]
                    }
                }
            }
        ],
        primary_action_label: __("Create"),
        primary_action: (args) => {
            if(!args) return;
            dialog.hide();

            return sub_rent_quotation(frm,args['supplier'])
        }
    });

    dialog.show()
    }, 'Create');
}

const sub_rent_quotation = (frm,args) => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Supplier Rental Quotation'),
			() => {
                const cur_doc = cur_frm.doc
                cur_doc.rental_order = doc.rental_order
                cur_doc.supplier = args
				cur_doc.items = []
				for (const row of doc.items) {
                    
					const new_row = cur_frm.add_child("items", {
						qty: row.qty,
                        description: row.description,
                        description_2: row.description_2
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
}