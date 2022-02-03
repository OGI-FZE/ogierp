frappe.ui.form.on("Supplier Quotation", {
    refresh(frm) {
        if (!frm.is_new()) {
            create_custom_buttons(frm)
        }
    }
})

const create_custom_buttons = (frm) => {
    create_pur_req(frm)
}

const create_pur_req = (frm) => {
    frappe.call({
            method: "frappe.desk.notifications.get_open_count",
            args: {
                "doctype": "Supplier Quotation",
                "name": cur_frm.doc.name,
                "items": ["Purchase Requisition"]
            },
            callback: function (data) {
                if((data.message.count[0].count) ==0){
                    frm.add_custom_button('Purchase Requisition', function() {
                        frappe.model.open_mapped_doc({
                            method: "oil_and_gas_international.events.supplier_quotation.make_purchase_requisition",
                            frm: frm
                        });
                    },__('Create'));
                }
            }
        });
}


