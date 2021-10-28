frappe.ui.form.on("Asset", {
    refresh(frm) {
        if (frm.doc.rental_status == "On hold for Inspection") {
            create_custom_buttons(frm)
        }
    }
})


const create_custom_buttons = (frm) => {
    frm.add_custom_button("Available for Rent", (frm) => {
        cur_frm.set_value("rental_status", "Available for Rent")
        cur_frm.savesubmit()
    })
}