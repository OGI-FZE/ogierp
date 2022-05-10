// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

var conv_rate = [1]
frappe.ui.form.on('Rental Timesheet', {
	rental_order(frm, cdt, cdn) {
		get_items_from_rental_order(frm, cdt, cdn)
		set_project(frm)
	},
	refresh:function(frm){
		if(frm.is_new()){
			frappe.model.set_value('Rental Timesheet',frm.doc.name,'status','Draft')
		}
		else if(frm.doc.docstatus==1){
			add_sales_invoice()
			// add_sales_order()
			add_proforma_invoice()
		}
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "base_operational_running","base_lihdbr","base_post_rental_inspection_charges","base_standby","base_straight","base_redress"
        	], company_currency, "items");
		var customer_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], customer_currency, "items");
	},
	onload(frm){
		if(frm.doc.customer && frm.doc.__islocal){
			frappe.db.get_value("Customer", {"name": frm.doc.customer}, "default_currency", (r) => {
				if(r.default_currency){
					frm.set_value("currency", r.default_currency)
				}
			});
		}
		get_conversion_rate(frm)
      	convert_rate(frm)
	},
	customer(frm){
		if(frm.doc.customer){
			frappe.db.get_value("Customer", {"name": frm.doc.customer}, "default_currency", (r) => {
				if(r.default_currency){
					frm.set_value("currency", r.default_currency)
				}
			});
		}
		get_conversion_rate(frm)
	},
	currency(frm){
		get_conversion_rate(frm)
		var customer_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], customer_currency, "items");

	},
	conversion_rate(frm){
    	convert_rate(frm)
  	},
	validate(frm){
		convert_rate(frm)
	}, 
	rental_order(frm, cdt, cdn) {
		get_items_from_rental_order(frm, cdt, cdn)
		set_project(frm)
	},
	calc_amount(frm,cdt, cdn){
		var items = frm.doc.items;
		var amnt = 0
		$.each(items, function(index, row){
			amnt = amnt + row.amount
		});
		frappe.model.set_value(cdt,cdn,'total_amount',amnt);
	}
	// setup(frm,cdt,cdn) {
	// 	frm.fields_dict['items'].grid.get_field('assets').get_query = function (doc, cdt, cdn) {
	// 		const row = locals[cdt][cdn]
	// 		return {
	// 			filters: {
	// 				rental_status: "In Use",
	// 				rental_order: frm.doc.rental_order,
	// 				docstatus:1
	// 			}
	// 		}
	// 	}
	// }
});

const convert_rate = function(frm){
  if(frm.doc.items && frm.doc.docstatus!=1){
    conv_rate.push(frm.doc.conversion_rate)
      for(let row of frm.doc.items){
        var converted_op_rate = (row.base_operational_running)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'operational_running',converted_op_rate)
        var converted_lihdbr_rate = (row.base_lihdbr)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'lihdbr',converted_lihdbr_rate)
        var converted_pr_rate = (row.base_post_rental_inspection_charges)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'post_rental_inspection_charges',converted_pr_rate)
        var converted_standby_rate = (row.base_standby)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'standby',converted_standby_rate)
        var converted_straight_rate = (row.base_straight)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'straight',converted_straight_rate)
        var converted_redress_rate = (row.base_redress)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'redress',converted_redress_rate)
        var converted_base_total_amount = (row.total_amount)*conv_rate[conv_rate.length-1]
        frappe.model.set_value(row.doctype,row.name,'base_total_amount',converted_base_total_amount)
      }
  }
}

const get_conversion_rate = (frm) => {
	let company_currency = erpnext.get_currency(frm.doc.company);
	frappe.call({
		method: "erpnext.setup.utils.get_exchange_rate",
		args: {
			from_currency: company_currency,
			to_currency: frm.doc.currency
		},
		callback: function(r) {
			if (r.message) {
				frm.set_value("conversion_rate",r.message)
			}
		}
	});
}

const get_items_from_rental_order = (frm, cdt, cdn) => {
	const rental_order = frm.doc.rental_order
	frm.call({
		method: "get_rental_order_items",
		args: { docname: rental_order },
		async: false,
		callback(res) {
			const data = res.message
			if (!data) return
			frm.doc.items = []
			for (const row of data) {
				if (!row.on_hold) {
					frm.call({
						method: "check_issue_note",
						args: { docname: rental_order,itm: row.item_code },
						async: false,
						callback(rti) {
							const issuenote=rti.message
							if (issuenote){
								for(let r = 0; r < issuenote.length; r++){
									// for(let i = 0; i < row.qty; i++){
									const new_row = frm.add_child('items', {
										'qty': 1,
										'asset_location': row.asset_location,
										'rental_order': rental_order,
										'rental_order_item': row.name,
										'operational_running':row.operational_running,
										'standby':row.standby,
										'lihdbr':row.lihdbr,
										'redress':row.redress,
										'straight':row.straight,
										'base_operational_running':row.base_operational_running,
										'base_standby':row.base_standby,
										'base_lihdbr':row.base_lihdbr,
										'base_redress':row.base_redress,
										'base_straight':row.base_straight,
										'assets':issuenote[r].assets,
									})
									const cdt = new_row.doctype
									const cdn = new_row.name
									frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
									// }
								}
							}
						}
					})
				}
			}

			cur_frm.refresh()
		}
	})
}


frappe.ui.form.on('Rental Timesheet Item', {
	operational_running_check: function(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.operational_running_check){
			frappe.model.set_value(cdt, cdn,"operational_running_days", row.days);
			frappe.model.set_value(cdt, cdn,"standby_days", '');
			frappe.model.set_value(cdt, cdn,"straight_days", '');
			frappe.model.set_value(cdt, cdn,"standby_check", 0);
    	frappe.model.set_value(cdt, cdn,"straight_check", 0);
		}
		else{
			frappe.model.set_value(cdt, cdn,"operational_running_days", '');
		}
  },
  standby_check: function(frm,cdt,cdn){
  	let row=locals[cdt][cdn]
  	if(row.standby_check){
  		frappe.model.set_value(cdt, cdn,"standby_days", row.days);
  		frappe.model.set_value(cdt, cdn,"operational_running_days", '');
  		frappe.model.set_value(cdt, cdn,"straight_days", '');
	    frappe.model.set_value(cdt, cdn,"operational_running_check", 0);
	    frappe.model.set_value(cdt, cdn,"straight_check", 0);
	  }
	  else{
			frappe.model.set_value(cdt, cdn,"standby_days", '');
		}
  },
  straight_check: function(frm,cdt,cdn){
  	let row=locals[cdt][cdn]
  	if(row.straight_check) {
  		frappe.model.set_value(cdt, cdn,"straight_days", row.days);
  		frappe.model.set_value(cdt, cdn,"standby_days", '');
  		frappe.model.set_value(cdt, cdn,"operational_running_days", '');
	    frappe.model.set_value(cdt, cdn,"operational_running_check", 0);
	    frappe.model.set_value(cdt, cdn,"standby_check", 0);
	  }
	  else{
			frappe.model.set_value(cdt, cdn,"straight_days", '');
		}
  },
  days: function(frm,cdt,cdn){
  	let row=locals[cdt][cdn]
  	if(row.operational_running_check){
			frappe.model.set_value(cdt, cdn,"operational_running_days", row.days);
			frappe.model.set_value(cdt, cdn,"standby_days", '');
			frappe.model.set_value(cdt, cdn,"straight_days", '');
			frappe.model.set_value(cdt, cdn,"standby_check", 0);
    	frappe.model.set_value(cdt, cdn,"straight_check", 0);
		}
		else{
			frappe.model.set_value(cdt, cdn,"operational_running_days", '');
		}
		if(row.straight_check) {
  		frappe.model.set_value(cdt, cdn,"straight_days", row.days);
  		frappe.model.set_value(cdt, cdn,"standby_days", '');
  		frappe.model.set_value(cdt, cdn,"operational_running_days", '');
	    frappe.model.set_value(cdt, cdn,"operational_running_check", 0);
	    frappe.model.set_value(cdt, cdn,"standby_check", 0);
	  }
	  else{
			frappe.model.set_value(cdt, cdn,"straight_days", '');
		}
		if(row.straight_check) {
  		frappe.model.set_value(cdt, cdn,"straight_days", row.days);
  		frappe.model.set_value(cdt, cdn,"standby_days", '');
  		frappe.model.set_value(cdt, cdn,"operational_running_days", '');
	    frappe.model.set_value(cdt, cdn,"operational_running_check", 0);
	    frappe.model.set_value(cdt, cdn,"standby_check", 0);
	  }
	  else{
			frappe.model.set_value(cdt, cdn,"straight_days", '');
		}
  },
  timesheet_end_date: function(frm,cdt,cdn){
  	let row = locals[cdt][cdn]
  	if(row.timesheet_start_date && row.timesheet_end_date){
  		if(row.timesheet_end_date < row.timesheet_start_date){
  			frappe.throw("End date can not be before start date!")
  		}
  		if(row.timesheet_start_date < frm.doc.start_date || row.timesheet_end_date > frm.doc.end_date){
  			frappe.throw("Please choose dates within the date range of timesheet: "+frm.doc.start_date+" to "+frm.doc.end_date)
  		}
  		frappe.model.set_value(cdt, cdn,"days", (frappe.datetime.get_day_diff(row.timesheet_end_date,row.timesheet_start_date))+1);

  	}
  },
  timesheet_start_date: function(frm,cdt,cdn){
  	let row = locals[cdt][cdn]
  	if(row.timesheet_start_date && row.timesheet_end_date){
  		if(row.timesheet_end_date < row.timesheet_start_date){
  			frappe.throw("End date can not be before start date!")
  		}
  		if(row.timesheet_start_date < frm.doc.start_date || row.timesheet_end_date > frm.doc.end_date){
  			frappe.throw("Please choose dates within the date range of timesheet: "+frm.doc.start_date+" to "+frm.doc.end_date)
  		}
  		frappe.model.set_value(cdt, cdn,"days", (frappe.datetime.get_day_diff( row.timesheet_end_date,row.timesheet_start_date))+1);
  	}
  },
	get_assets(frm, cdt, cdn) {
		get_assets_to_receive(frm, cdt, cdn)   
	},
	qty(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.qty){
			calculate_amount(frm,cdt,cdn)
		}
	},
	operational_running_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.operational_running_days){
			calculate_amount(frm,cdt,cdn)
		}
	},
	standby_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
			if(row.standby_days){
				console.log('working');
				calculate_amount(frm,cdt,cdn)
			}
	},
	redress_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.redress_days){
			calculate_amount(frm,cdt,cdn)
		}
	},
	lihdbr_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.lihdbr_days){
			calculate_amount(frm,cdt,cdn)
		}
	},
	straight_days(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.straight_days){
			calculate_amount(frm,cdt,cdn)
		}
	},
	operational_running(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.operational_running){
			calculate_amount(frm,cdt,cdn)
		}
	},
	standby(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.standby){
			calculate_amount(frm,cdt,cdn)
		}
	},
	redress(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.redress){
			calculate_amount(frm,cdt,cdn)
		}
	},
	lihdbr(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.lihdbr){
			calculate_amount(frm,cdt,cdn)
		}
	},
	straight(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.straight){
			calculate_amount(frm,cdt,cdn)
		}
	},
	post_rental_inspection_charges(frm,cdt,cdn){
		let row=locals[cdt][cdn]
		if(row.post_rental_inspection_charges){
			calculate_amount(frm,cdt,cdn)
		}
	},
	amount(frm,cdt,cdn){
		frm.trigger('calc_amount');
	}
});

const calculate_amount=(frm,cdt,cdn)=>{
	let row= locals[cdt][cdn]
	let total=0
	if(row.operational_running_check && row.operational_running_days && row.operational_running>0){
		total = row.operational_running_days*row.operational_running
		console.log(total);
	}
	if(row.standby_check && row.standby_days && row.standby>0){
		total = total +( row.standby_days*row.standby)
		console.log(total);
	}
	if(row.redress_days && row.redress>0){
		total = total+ (row.redress)
		console.log(total);
	}
	if(row.lihdbr_days && row.lihdbr>0){
		total = total+ (row.lihdbr)
		console.log(total);
	}
	if(row.straight_check && row.straight_days && row.straight>0){
		total = total+ ( row.straight_days*row.straight)
		console.log(total);
	}
	if(row.post_rental_inspection_charges >0){
		total = total+ ( row.post_rental_inspection_charges)
		console.log(total);
	}
	frappe.model.set_value(cdt,cdn,'amount',total*row.qty)
	convert_rate(frm)

}

const get_assets_to_receive = (frm, cdt, cdn) => {
	const doctype = "Asset"
	new frappe.ui.form.MultiSelectDialog({
		doctype: doctype,
		target: this.cur_frm,
		setters: {
			asset_name: null,
		},
		date_field: "transaction_date",
		get_query() {
			return {
				filters: {
					rental_status: "In Use",
					rental_order: frm.doc.rental_order
				}
			}
		},
		action(selections) {
			const cur_row = locals[cdt][cdn]
			let serial_nos = ""
			for (const row of selections) {
				serial_nos += row + "\n"
			}

			cur_row.assets = serial_nos
			cur_frm.refresh()
			cur_dialog.hide()
		}
	});
}

const set_project = (frm) => {
	const rental_order = frm.doc.rental_order
	frappe.call({
		method: "oil_and_gas_international.oil_and_gas_international.doctype.rental_issue_note.rental_issue_note.get_project",
		args: { docname: rental_order },
		async: false,
		callback(res){
			const data = res.message
			frm.set_value("project", data.name)
		}
	})
}

const add_sales_invoice = () => {
	cur_frm.add_custom_button('Sales Invoice', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Sales Invoice'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				// cur_doc.rental_timesheet = doc.name
				cur_doc.rental_order = doc.rental_order
				cur_doc.departments = doc.departments
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_timesheet", doc.name)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "currency", doc.currency)
				cur_doc.items = []
				console.log("itemss",doc.items)
				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						qty: row.qty,
						asset_item:row.item_code,
						rental_order:row.rental_order,
						rental_order_item:row.rental_order_item,
						assets:row.assets
					})
					console.log("new_row",new_row)
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
					setTimeout(function(){
						frappe.model.set_value(cdt, cdn, "price_list_rate",row.amount)
						frappe.model.set_value(cdt, cdn, "rate",row.amount)
						frappe.model.set_value(cdt, cdn, "amount",row.amount)
					}, 2000);
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_sales_order = () => {
	cur_frm.add_custom_button('Sales Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Sales Order'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				// cur_doc.rental_timesheet = doc.name
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				cur_doc.rental_order = doc.rental_order
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_timesheet", doc.name)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "currency", doc.currency)
				cur_doc.items = []

				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						qty: row.qty,
						asset_item:row.item_code,
						rental_order:row.rental_order,
						rental_order_item:row.rental_order_item,
						assets:row.assets,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
					frappe.model.set_value(cdt, cdn, "item_name",'Asset Rent Item')
					setTimeout(function(){
						frappe.model.set_value(cdt, cdn, "price_list_rate",row.amount)
						frappe.model.set_value(cdt, cdn, "rate",row.amount)
						frappe.model.set_value(cdt, cdn, "amount",row.amount)
					}, 2000);
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_proforma_invoice = () => {
	cur_frm.add_custom_button('Proforma Invoice', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Proforma Invoice'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				// cur_doc.rental_timesheet = doc.name
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				cur_doc.rental_order = doc.rental_order
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_timesheet", doc.name)
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "currency", doc.currency)
				cur_doc.items = []

				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						asset_item:row.item_code,
						rental_order:row.rental_order,
						rental_order_item:row.rental_order_item,
						assets:row.assets,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
					frappe.model.set_value(cdt, cdn, "item_name",'Asset Rent Item')
					setTimeout(function(){
						frappe.model.set_value(cdt, cdn, "price_list_rate",row.amount)
						frappe.model.set_value(cdt, cdn, "rate",row.amount)
						frappe.model.set_value(cdt, cdn, "amount",row.amount)
					}, 2000);
				}

				cur_frm.refresh()
			}
		])
	}, 'Create')
}
