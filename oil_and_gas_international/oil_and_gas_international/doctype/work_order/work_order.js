// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Work_Order', {
	refresh: function(frm) {
		frm.set_query('party_type', () => {
			return {
				filters: {
					name: ['in', ['Customer','Supplier']]
				}
			};
		});
	},
	party: function(frm) {
		if(frm.doc.party && frm.doc.party_type){
			var party_nm = (String(frm.doc.party_type).toLowerCase()).concat("_name")
			frappe.db.get_value(frm.doc.party_type, frm.doc.party, party_nm, (r) => {				
				if(r){
					if(frm.doc.party_type === 'Customer'){
						frm.set_value("party_name",r.customer_name);
					}
					if(frm.doc.party_type === 'Supplier'){
						frm.set_value("party_name",r.supplier_name);
					}
				}
			})
		}
	}
});
