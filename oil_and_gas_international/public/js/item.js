frappe.ui.form.on("Item", {
    setup(frm) {
        set_query(frm)
    },
    // item_group:function(frm,dt,dn){
    //     if(frm.doc.item_group){
    //         frappe.db.get_doc('Item Group', frm.doc.item_group)
    //         .then(doc => {
    //             if(doc){
    //                 if(doc.is_group){
    //                     frappe.msgprint('Please select a chlild group.')
    //                     frappe.model.set_value(dt,dn,'item_group','')
    //                 }else{
    //                     frappe.model.set_value(dt,dn,'parent_group','')
    //                     frappe.db.get_doc('Item Group', doc.parent_item_group)
    //                     .then(par_doc => {
    //                         frappe.model.set_value(dt,dn,'parent_group',par_doc.name)
    //                         frappe.model.set_value(dt,dn,'grand_parent_group','')
    //                         if(par_doc.parent_item_group){
    //                             frappe.db.get_doc('Item Group', par_doc.parent_item_group)
    //                             .then(gpar_doc => {
    //                                 if(gpar_doc){
    //                                     frappe.model.set_value(dt,dn,'grand_parent_group',gpar_doc.name)
    //                                 }
    //                             })
    //                         }
    //                     })
    //                 }
    //             }
    //         })
    //     }
    // }
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