frappe.ui.form.on("Opportunity", {
    refresh(frm) {
        if (!frm.is_new()) {
            create_custom_buttons(frm)
        }
    }
})

frappe.ui.form.on("Opportunity Item", {
    item_code(frm, cdt, cdn) {
        const row = locals[cdt][cdn]
        const item_code = row.item_code
        frappe.db.get_value("Item", item_code, "item_type").then(r => {
            row.item_type = r.message.item_type
            frm.refresh()
        })
    },
    
    item_type(frm) {
        frm.fields_dict['items'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
            return {
                filters: [
                    ['item_type', '=', locals[cdt][cdn].item_type]
                ]
            }
        }
    },
})

const create_custom_buttons = (frm) => {
    create_estimation(frm)
    create_rental_estimation(frm)
    create_rental_quotation(frm)
}

const create_rental_estimation = (frm) => {
    frm.add_custom_button('Rental Estimation', () => {
        const doc = frm.doc;
        frappe.run_serially([
            () => frappe.new_doc('Rental Estimation'),
            () => {
                cur_frm.doc.customer = doc.party_name;
                cur_frm.doc.customer_name = doc.customer_name;
                cur_frm.doc.date = doc.transaction_date;
                cur_frm.doc.valid_till = doc.expected_closing;
                cur_frm.doc.opportunity = doc.name;
                cur_frm.doc.items = []
                for (let row of doc.items) {
                    if (row.item_type == 'Rental') {
                        const new_row = cur_frm.add_child('items', {
                            'qty': row.qty,
                            'item_name': row.item_name,
                            'description': row.description,
                            'opportunity': doc.name,
                        })
                        const cdt = new_row.doctype
                        const cdn = new_row.name
                        frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                    }

                }

                cur_frm.refresh()
            }
        ])
    }, 'Create');
}

const create_estimation = (frm) => {
    if (!frm.doc.__islocal && frm.doc.docstatus == 0 && frm.doc.with_items) {
        frm.add_custom_button(__('Estimation Sheet'),
            function() {
                frappe.model.open_mapped_doc({
                    method: "oil_and_gas_international.oil_and_gas_international.doctype.estimation_sheet.estimation_sheet.make_estimation",
                    frm: frm
                })
            }, __("Create"), "btn-default");
    }
}

const create_rental_quotation = (frm) => {
    frm.add_custom_button('Rental Quotation', () => {
        const doc = frm.doc;
        frappe.run_serially([
            () => frappe.new_doc('Rental Quotation'),
            () => {
                cur_frm.doc.customer = doc.party_name;
                cur_frm.doc.customer_name = doc.customer_name;
                cur_frm.doc.date = doc.posting_date;
                cur_frm.doc.valid_till = doc.expected_closing;
                cur_frm.doc.departments = doc.departments;
                cur_frm.doc.sales_person = doc.sales_person;
                cur_frm.doc.opportunity = doc.name;
                cur_frm.doc.items = []
                for (let row of doc.items) {
                    if (row.item_type == 'Rental') {
                        const new_row = cur_frm.add_child('items', {
                            'qty': row.qty,
                            'item_name': row.item_name,
                            'description': row.description,
                            'uom': row.uom,
                            'rate': row.basic_rate,
                            // 'opportunity': doc.name,
                        })
                        const cdt = new_row.doctype
                        const cdn = new_row.name
                        frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                    }

                }

                cur_frm.refresh()
            }
        ])
    }, 'Create');
}