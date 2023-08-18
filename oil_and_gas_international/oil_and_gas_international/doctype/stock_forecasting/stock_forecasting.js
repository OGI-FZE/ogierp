// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Stock Forecasting', {
	// refresh: function(frm) {

	// }
	quantity:function(frm) {
		set_amount(frm)
	},
	rate : function(frm){
		set_amount(frm)
	},
	forcast_type: function(frm){
		set_forcast_type_label(frm)
	},
	item_type: function(frm){
		frappe.run_serially([
            () => set_uom(frm),
            () => set_item_group(frm),
		])
	}
});

var set_amount = function(frm){
	if (frm.doc.quantity && frm.doc.rate){
		let amount = frm.doc.quantity * frm.doc.rate
		frm.set_value("total",amount)
	}
}

var set_exchange_rate_label = function(frm){
	if(frm.doc.base_currency && frm.doc.quote_currency) {
	  var default_label = __(frappe.meta.docfield_map[cur_frm.doctype]["quote_conversion"].label);
	  cur_frm.fields_dict.quote_conversion.set_label(default_label +
		repl(" (1 %(base_currency)s = [?] %(quote_currency)s)", cur_frm.doc));
	}
  }

var set_forcast_type_label = function(frm) {
	if(frm.doc.forcast_type){
		if(frm.doc.forcast_type == "Item"){
			cur_frm.fields_dict.item_type.set_label(repl("Item", cur_frm.doc));
		}
		else if(frm.doc.forcast_type == "Item Group"){
			cur_frm.fields_dict.item_type.set_label(repl("Item Group", cur_frm.doc));
		}
	}
}

var set_uom = function(frm){
	if(frm.doc.forcast_type && frm.doc.item_type){
		if(frm.doc.forcast_type == "Item"){
			frappe.db.get_value('Item', {"name": frm.doc.item_type}, 'stock_uom', (value) => {
				frm.set_value("uom", value.stock_uom);
			});
		}
		else{
			frm.set_value("uom", '');
		}
	}
}

var set_item_group = function(frm){
	if(frm.doc.forcast_type && frm.doc.item_type){
		if(frm.doc.forcast_type == "Item"){
			frappe.db.get_value('Item', {"name": frm.doc.item_type}, 'item_group', (value) => {
				frm.set_value("item_group", value.item_group);
			});
		}
		else{
			frm.set_value("item_group", '');
		}
	}
}