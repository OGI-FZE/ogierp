// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Estimation', {
	setup(frm){
        frm.fields_dict['items'].grid.get_field('item_code').get_query = function(doc, cdt, cdn) {
            return {    
                filters:[
                    ['item_type', '=', 'Rental']
                ]
            }
        }
    },
	refresh(frm){
		if(frm.doc.docstatus==0){
			custom_buttom(frm)
		}
	}
});

frappe.ui.form.on('Rental Estimation Item', {
	quantity: function(frm,cdt,cdn) {
		calc_amount(frm,cdt,cdn)
		calc_total_amount(frm)
	},
	estimate_rate:function(frm,cdt,cdn){
		calc_amount(frm,cdt,cdn)
		calc_total_amount(frm)
	},
	total: function(frm,cdt,cdn) {
		console.log('workign');
		calc_total_amount(frm)
	},
});

//Helping Functions
const calc_amount=(frm,cdt,cdn)=>{
	let row= locals[cdt][cdn]
	frappe.model.set_value(cdt,cdn,'amount',row.quantity*row.estimate_rate)
}
const calc_total_amount=(frm)=>{
	let total=0
	for(let row of frm.doc.items){
		if(row.amount){
			total+=row.amount
		}
	}
	frappe.model.set_value('Rental Estimation',frm.doc.name,'total',total)
}
const custom_buttom=(frm)=>{
    frm.add_custom_button('Opportunity', () => {
        
    }, 'Get Items From');
    
}