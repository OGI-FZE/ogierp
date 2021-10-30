frappe.ui.form.on("Item", {
    setup(frm) {
        set_query(frm)
    }
})


const set_query = frm => {
    frm.set_query("relevant_item", () => {
        return {
            filters: {
                is_stock_item: 1,
                is_fixed_asset: 0,
                has_serial_no: 1,
            }
        }
    })
}