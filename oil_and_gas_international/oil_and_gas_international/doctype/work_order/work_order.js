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

frappe.ui.form.on('Workorder item', {
	get_assets(frm, cdt, cdn) {
		get_assets_to_issue(frm, cdt, cdn)
	}
});

const get_assets_to_issue = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]

	const doctype = "Asset"
	new frappe.ui.form.MultiSelectDialog({
		doctype: doctype,
		target: this.cur_frm,
		setters: {
			asset_name: null
		},
		date_field: "transaction_date",
		get_query() {
			let asset_list = []
			let filters = {};
			$.each(frm.doc.items, function(_idx, val) {
				if (val.assets) asset_list.push(val.assets);
			});
		    if(asset_list.length){
		    	if(frm.doc.rental_order){
		    		filters['rental_status'] = ["in","Available For Rent","On hold for Inspection"];
		    	}
		    	if(frm.doc.sub_rental_order){
		    		filters['rental_status'] = "On hold for Inspection";
		    	}
		    	filters['item_code'] = row.item_code;
		    	filters['docstatus'] = 1;
		    	filters['name'] = ['not in',asset_list];
		    }
		    else{
		    	if(frm.doc.rental_order){
		    		filters['rental_status'] = ["in","Available For Rent","On hold for Inspection"];
		    	}
		    	if(frm.doc.sub_rental_order){
		    		filters['rental_status'] = "On hold for Inspection";
		    	}
		    	filters['item_code'] = row.item_code;
		    	filters['docstatus'] = 1;
		    }
			return {
				filters: filters
			}
		},
		action(selections) {
			const cur_row = locals[cdt][cdn]
			let serial_nos = ""
			if(selections.length != cur_row.quantity){
				frappe.msgprint(__("Warning! Required number of assets should be same as the quantity: ")+cur_row.quantity)
			}
			for (const row of selections) {
				serial_nos += row + "\n"
			}

			cur_row.assets = serial_nos
			cur_frm.refresh()
			cur_dialog.hide()
		}
	});
}