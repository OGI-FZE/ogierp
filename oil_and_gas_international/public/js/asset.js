frappe.ui.form.on("Asset", {
    refresh(frm) {
        if (frm.doc.rental_status == "On hold for Inspection") {
            create_custom_buttons(frm)
        }
    },
    validate(frm) {
        if(frm.doc.purchase_receipt){
            frappe.db.get_value('Purchase Receipt', frm.doc.purchase_receipt, "supplier", function(value) {
                frappe.model.set_value('Asset',frm.doc.name,'supplier_info',value['supplier'])
            });
        }
        if(frm.doc.purchase_invoice){
            frappe.db.get_value('Purchase Invoice', frm.doc.purchase_invoice, "supplier", function(value) {
                frappe.model.set_value('Asset',frm.doc.name,'supplier_info',value['supplier'])
            });
        }
    }
})


const create_custom_buttons = (frm) => {
    frm.add_custom_button("Available for Rent", (frm) => {
        cur_frm.set_value("rental_status", "Available for Rent")
        cur_frm.savesubmit()
    })
}