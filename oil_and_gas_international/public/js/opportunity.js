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
    },
    
})
frappe.ui.form.on("Opportunity", {
    refresh(frm){
        if(frm.doc.docstatus==0){
            console.log('working');
            custom_buttom(frm)
        }
    }
})
const custom_buttom=(frm)=>{
    frm.add_custom_button('Rental Estimation', () => {
        const doc = frm.doc;
		frappe.run_serially([
		() => frappe.new_doc('Rental Estimation'),
		() => {
			cur_frm.doc.customer = doc.party_name;
            cur_frm.doc.customer_name = doc.customer_name;
			cur_frm.doc.date = doc.transaction_date;
			cur_frm.doc.valid_till = doc.valid_till;
			cur_frm.doc.opportunity = doc.name;
			cur_frm.doc.items = []
			for(let row of doc.items){
                if(row.item_type=='Rental'){
                    let new_row = cur_frm.add_child('items', {
                        'quantity': row.qty,
                        'item_code':row.item_code,
                        'item_name':row.item_name,
                        'description':row.description
                    })
                }
				
			}
			
			cur_frm.refresh()
		}
		])
        
    }, 'Create');
    
}