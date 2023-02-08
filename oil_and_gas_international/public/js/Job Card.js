frappe.ui.form.on("Job Card", {
    refresh(frm) {
        if (frm.doc.docstatus == 0) {
            add_inspection()
            }
    },

    // onload(frm) {
        // console.log('dddddddd')
        // frm.operation = frm.operation
        // frm.refresh()
    
})

const add_inspection = () => {
    cur_frm.add_custom_button('Create Inspection', () => {
		const doc = cur_frm.doc
        frappe.run_serially([
                            () => frappe.new_doc('Inspection'),
                            () => {
                            frappe.db.get_value("Work Order",{'name':doc.work_order,'production_item':doc.production_item},
                            ["project_wo","project","qty","fg_warehouse","sales_order","rental_order","item_category"], (r) => {
                                const cur_doc = cur_frm.doc
                                cur_doc.item_code = doc.production_item
                                cur_doc.quantity = r.qty
                                cur_doc.item_category = r.item_category
                                cur_doc.warehouse = r.fg_warehouse
                                cur_doc.project_ = r.project
                                cur_doc.work_order = doc.work_order
                                cur_doc.project_work_order = r.project_wo
                                cur_doc.sales_order = r.sales_order
                                cur_doc.rental_order = r.rental_order
                                
                                cur_frm.set_df_property('item_category', 'read_only', 1);
                                
                                cur_frm.refresh()
                            })
                        }
                        ])
    
});
}