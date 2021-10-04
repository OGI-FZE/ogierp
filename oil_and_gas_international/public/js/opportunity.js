frappe.ui.form.on("Opportunity Item", {
    item_type(frm,cdt,cdn){
        let row=locals[cdt][cdn]
        frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
            return {    
                filters:[
                    ['item_type', '=', row.item_type]
                ]
            }
        }
    }
})