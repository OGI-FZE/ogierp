// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Rental Quotation', {
	before_submit:function(frm){
		console.log('submit');
		frappe.model.set_value('Rental Quotation',frm.doc.name,'status','Open')
	},
	refresh(frm){
		if(frm.doc.docstatus==0){
			custom_buttom(frm)
		}
	}
});
frappe.ui.form.on('Rental Quotation Item', {
	quantity: function(frm,cdt,cdn) {
		calc_amount(frm,cdt,cdn)
		calc_total_amount(frm)
	},
	rate:function(frm,cdt,cdn){
		calc_amount(frm,cdt,cdn)
		calc_total_amount(frm)
	},
	total: function(frm,cdt,cdn) {
		calc_total_amount(frm)
	},
});
const calc_amount=(frm,cdt,cdn)=>{
	console.log('working');
	let row= locals[cdt][cdn]
	frappe.model.set_value(cdt,cdn,'amount',row.quantity*row.rate)
}
const calc_total_amount=(frm)=>{
	let total=0
	for(let row of frm.doc.items){
		if(row.amount){
			total+=row.amount
		}
	}
	frappe.model.set_value('Rental Quotation',frm.doc.name,'total',total)
}
const custom_buttom=(frm)=>{
    frm.add_custom_button('Rental Estimation', () => {
        
    }, 'Get Items From');
    
}