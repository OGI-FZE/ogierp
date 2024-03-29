frappe.ui.form.on("Opportunity", {
    refresh(frm) {
        if (!frm.is_new()) {
            create_custom_buttons(frm)
        }
    },
    validate(frm){
        if (frm.doc.with_items){
		frm.doc.items.forEach(function(item){
            frappe.db.get_value("Item", item.item_code, "description", (r) => {
                console.log(r.description)
                if (!item.description_2){
                    frappe.model.set_value(item.doctype, item.name, 'description_2',r.description);
                }

            })
		})
  	}
}
})

    

// frappe.ui.form.on("Opportunity Item", {
//     item_code(frm, cdt, cdn) {
//         const row = locals[cdt][cdn]
//         const item_code = row.item_code
//         frappe.db.get_value("Item", item_code, "item_type").then(r => {
//             row.item_type = r.message.item_type
//             frm.refresh()
//         })
//     },
    
//     item_type(frm) {
//         frm.fields_dict['items'].grid.get_field('item_code').get_query = function (doc, cdt, cdn) {
//             return {
//                 filters: [
//                     ['item_type', '=', locals[cdt][cdn].item_type]
//                 ]
//             }
//         }
//     },
// })

const create_custom_buttons = (frm) => {
    create_estimation(frm)
    create_rental_estimation(frm)
    create_rfq(frm)
    create_rental_quotation(frm)
    create_tender(frm)
}

const create_rental_estimation = (frm) => {
    frm.add_custom_button('Rental Estimation', () => {
        const doc = frm.doc;
        frappe.run_serially([
            () => frappe.new_doc('Rental Estimation'),
            () => {
                cur_frm.doc.departments = doc.departments;
                if (doc.opportunity_from == "Customer"){
                    cur_frm.doc.customer = doc.party_name;
                    cur_frm.doc.customer_name = doc.customer_name;
                }
                else {
                    cur_frm.doc.lead = doc.party_name;
                    cur_frm.doc.lead_name = doc.lead_name;
                }
                cur_frm.doc.customer = doc.party_name;
                cur_frm.doc.date = doc.transaction_date;
                cur_frm.doc.valid_till = doc.expected_closing;
                cur_frm.doc.opportunity = doc.name;
                cur_frm.doc.division = doc.division;
                cur_frm.doc.sales_person = doc.sales_person;
                cur_frm.doc.customer_reference = doc.customer_reference;
                cur_frm.doc.enquery_no = doc.enquery_no;
                cur_frm.doc.enquery_ref = doc.enquery_ref;
                cur_frm.doc.estimation_to = doc.opportunity_from;
                cur_frm.doc.departments = doc.department
                cur_frm.doc.items = []
                for (let row of doc.items) {
                        const new_row = cur_frm.add_child('items', {
                            'description_2_': row.description_2,
                            'item_name': row.item_name,
                            'qty': row.qty,
                            'uom': row.uom,
                            'description': row.description,
                            'item_name': row.item_name,
                            'opportunity': cur_frm.doc.opportunity,
                            'customer_requirement': row.customer_requirement,
                        })
                        const cdt = new_row.doctype
                        const cdn = new_row.name
                        frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                }

                cur_frm.refresh()
            }
        ])
    }, 'Create');
}

const create_rfq = (frm) => {
    frm.add_custom_button('Request For Quotation', () => {
        const doc = frm.doc;
        frappe.run_serially([
            () => frappe.new_doc('Request for Quotation'),
            () => {
                cur_frm.doc.items = []
                cur_frm.doc.department = doc.department
                for (let row of doc.items) {
                        const new_row = cur_frm.add_child('items', {
                            'qty': row.qty,
                            'description': row.description,
                            'description_2': row.description_2
                        })
                        const cdt = new_row.doctype
                        const cdn = new_row.name
                        row.
                        frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                }

                cur_frm.refresh()
            }
        ])
    }, 'Create');
}

const create_tender = (frm) => {
    frm.add_custom_button('Tender', () => {
        const doc = frm.doc;
        frappe.run_serially([
            () => frappe.new_doc('Tender'),
            () => {
                if (doc.opportunity_from == "Lead"){
                    frappe.model.set_value('Tender',cur_frm.doc.name,"tender_against", "Lead")
					frappe.model.set_value('Tender',cur_frm.doc.name,"lead", doc.party_name)
                }
                else{
                    frappe.model.set_value('Tender',cur_frm.doc.name,"tender_against", "Customer")
                    frappe.model.set_value('Tender',cur_frm.doc.name,"customer", doc.party_name)
                }
                cur_frm.doc.department = doc.department;
                cur_frm.doc.customer = doc.party_name;
                cur_frm.doc.division = doc.division;
                cur_frm.doc.customer_reference = doc.customer_reference;
                cur_frm.doc.opportunity = doc.name;
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
                    method: "oil_and_gas_international.events.shared.make_estimation",
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
                if (doc.opportunity_from == "Customer"){
                    cur_frm.doc.customer = doc.party_name;
                    cur_frm.doc.customer_name = doc.customer_name;
                }
                else {
                    cur_frm.doc.lead = doc.party_name;
                    cur_frm.doc.lead_name = doc.customer_name;
                }
                cur_frm.doc.date = doc.transaction_date;
                cur_frm.doc.valid_till = doc.expected_closing;
                cur_frm.doc.division = doc.division;
                cur_frm.doc.departments = doc.department;
                cur_frm.doc.sales_person = doc.sales_person;
                cur_frm.doc.opportunity = doc.name;
                cur_frm.doc.division = doc.division;
                cur_frm.doc.customer_reference = doc.customer_reference
                cur_frm.doc.enquery_no = doc.enquery_no
                cur_frm.doc.enquery_ref = doc.enquery_ref
                cur_frm.doc.estimation_to = doc.opportunity_from;

                cur_frm.doc.items = []
                for (let row of doc.items) {
                        const new_row = cur_frm.add_child('items', {
                            'description_2': row.description_2,
                            'item_name': row.item_name,
                            'qty': row.qty,
                            'uom': row.uom,
                            'description': row.description,
                            'opportunity': cur_frm.doc.opportunity,
                            'customer_requirement': row.customer_requirement,
                            // 'opportunity': doc.name,
                        })
                        const cdt = new_row.doctype
                        const cdn = new_row.name
                        frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
                }

                cur_frm.refresh()
            }
        ])
    }, 'Create');
}