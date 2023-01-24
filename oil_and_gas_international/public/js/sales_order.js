frappe.ui.form.on("Sales Order", {
    refresh(frm) {
        if (!frm.is_new()) {
            create_custom_buttons(frm)
        }
        // frm.call({
        //     method: "oil_and_gas_international.events.sales_order.get_weight",
        //     args: { docname: frm.doc.name },
        //     callback(res){
        //         frm.refresh_field("items")
        //     }
        // })
    },
    rental_timesheet(frm) {
        if(frm.doc.rental_timesheet){
            set_project(frm)
        }
    },
})

const create_custom_buttons = (frm) => {
    create_workorder(frm)
    create_proforma(frm)
    create_contract_checklist(frm)

}

const create_contract_checklist = (frm) => {

    frm.add_custom_button('Contract Review Checklist', () => {
        const doc = frm.doc;
        frappe.run_serially([
            () => frappe.new_doc('Contract Review Checklist'),
            () => {
                //cur_frm - work order doc-so
                cur_frm.doc.date = doc.transaction_date;
                cur_frm.doc.customer = doc.customer;
                cur_frm.doc.enquiry_no = doc.po_no;
                cur_frm.refresh()
            }
        ])
    }, 'Create');
}


const create_workorder = (frm) => {
    var proj = ''
    frappe.db.get_list("Project", {
        filters: { 'sales_order': ["=", frm.doc.name]},
        fields: ["name"]
    }).then((data) =>{
        proj = data[0].name
    })
    frm.add_custom_button('Work-Order', () => {
        const doc = frm.doc;
        frappe.run_serially([
            () => frappe.new_doc('Work_Order'),
            () => {
                //cur_frm - work order doc-so
                cur_frm.doc.party_type = "Customer";
                cur_frm.doc.party = doc.customer;
                cur_frm.doc.party_name = doc.customer_name;
                cur_frm.doc.company = doc.company;
                cur_frm.doc.date = doc.transaction_date;
                cur_frm.doc.sales_order = doc.name;
                cur_frm.doc.po_number = doc.po_no;
                cur_frm.doc.po_date = doc.po_date;
                cur_frm.doc.job_number = proj;
                cur_frm.doc.items = []
                for (let row of doc.items) {
                    cur_frm.add_child('items', {
                        'quantity': row.qty,
                        'item_code': row.item_code,
                        'item_name': row.item_name,
                        'description': row.description,
                        'item_group': row.item_group,
                        'stock_uom': row.stock_uom,
                        'uom': row.uom,
                        'uom_conversion_factor': row.conversion_factor,
                        'stock_qty': row.stock_qty,
                    })
                }

                cur_frm.refresh()
            }
        ])
    }, 'Create');
}

const set_project = (frm) => {
    frappe.db.get_value('Rental Timesheet', {'name':frm.doc.rental_timesheet}, 'rental_order', (r) => {
        if(r && r.rental_order){
            const rental_order = r.rental_order
            frm.call({
                method: "oil_and_gas_international.oil_and_gas_international.doctype.rental_issue_note.rental_issue_note.get_project",
                args: { docname: rental_order },
                async: false,
                callback(res){
                    const data = res.message
                    frm.set_value("project", data.name)
                }
            })
        }
        
    });
}

const create_proforma = (frm) => {
    frappe.call({
            method: "frappe.desk.notifications.get_open_count",
            args: {
                "doctype": "Sales Order",
                "name": cur_frm.doc.name,
                "items": ["Proforma Invoice"]
            },
            callback: function (data) {
                if((data.message.count[0].count) ==0){
                    frm.add_custom_button('Proforma Invoice', function() {
                        frappe.model.open_mapped_doc({
                            method: "oil_and_gas_international.events.sales_order.make_proforma_invoice",
                            frm: frm
                        });
                    },__('Create'));

                }
            }
        });
}