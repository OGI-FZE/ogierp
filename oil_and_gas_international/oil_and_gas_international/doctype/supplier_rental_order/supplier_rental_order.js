// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

var conv_rate = [1]

frappe.ui.form.on('Supplier Rental Order', {
	refresh(frm) {
		if (frm.doc.docstatus ==1){
			add_material_receipt(frm)
			add_subrental_timesheet(frm)
		}
		// create_custom_buttons(frm)
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "base_operational_running","base_lihdbr","base_post_rental_inspection_charges","base_standby","base_straight","base_redress","base_total_amount"
        	], company_currency, "items");
		var billing_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress","total_amount"
        ], billing_currency, "items");
	},
	onload(frm){
		if(frm.doc.supplier && frm.doc.__islocal){
			frappe.db.get_value("Supplier", {"name": frm.doc.supplier}, "default_currency", (r) => {
				if(r.default_currency){
					frm.set_value("currency", r.default_currency)
				}
			});
		}
		get_conversion_rate(frm)
      	convert_rate(frm)
	},
	supplier(frm){
		if(frm.doc.supplier){
			frappe.db.get_value("Supplier", {"name": frm.doc.supplier}, "default_currency", (r) => {
				if(r.default_currency){
					frm.set_value("currency", r.default_currency)
				}
			});
		}
		get_conversion_rate(frm)
	},
	currency(frm){
		get_conversion_rate(frm)
		var billing_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress","total_amount"
        ], billing_currency, "items");

	},
	conversion_rate(frm){
    	convert_rate(frm)
  	},
  	validate(frm){
		frm.doc.items.forEach(function(item){
			if (item.operational_running != 0){
				frappe.model.set_value(item.doctype, item.name, 'base_operational_running', item.operational_running/frm.doc.conversion_rate);
			}
			else {
				frappe.model.set_value(item.doctype, item.name, 'operational_running', item.base_operational_running* frm.doc.conversion_rate);
			}
			if (item.lihdbr != 0){
				frappe.model.set_value(item.doctype, item.name, 'base_lihdbr', item.lihdbr/ frm.doc.conversion_rate);
			}
			else {
				frappe.model.set_value(item.doctype, item.name, 'lihdbr', item.base_lihdbr* frm.doc.conversion_rate);
			}
			if (item.post_rental_inspection_charges != 0){
				frappe.model.set_value(item.doctype, item.name, 'base_post_rental_inspection_charges', item.post_rental_inspection_charges/ frm.doc.conversion_rate);
			}
			else {
				frappe.model.set_value(item.doctype, item.name, 'post_rental_inspection_charges', item.base_post_rental_inspection_charges* frm.doc.conversion_rate);
			}
			if (item.standby != 0){
				frappe.model.set_value(item.doctype, item.name, 'base_standby', item.standby/ frm.doc.conversion_rate);
			}
			else {
				frappe.model.set_value(item.doctype, item.name, 'standby', item.base_standby* frm.doc.conversion_rate);
			}
			if (item.straight != 0){
				frappe.model.set_value(item.doctype, item.name, 'base_straight', item.straight/ frm.doc.conversion_rate);
			}
			else {
				frappe.model.set_value(item.doctype, item.name, 'straight', item.base_straight* frm.doc.conversion_rate);
			}
			if (item.redress != 0){
				frappe.model.set_value(item.doctype, item.name, 'base_redress', item.redress/ frm.doc.conversion_rate);
			}
			else {
				frappe.model.set_value(item.doctype, item.name, 'redress', item.base_redress* frm.doc.conversion_rate);
			}

		}),
  	 	convert_rate(frm)
  	}
});

const convert_base_rate = function(frm){
	if(frm.doc.items && frm.doc.docstatus!=1){
	  conv_rate.push(frm.doc.conversion_rate)
		for(let row of frm.doc.items){
		 // var converted_op_rate = (row.base_operational_running)*conv_rate[conv_rate.length-1]
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

  const convert_rate = function(frm){
	if(frm.doc.items && frm.doc.docstatus!=1){
	  conv_rate.push(frm.doc.conversion_rate)
		for(let row of frm.doc.items){
		  var converted_op_rate = (row.operational_running)*conv_rate[conv_rate.length-1]
		  // frappe.model.set_value(row.doctype,row.name,'base_operational_running',converted_op_rate)
		  var converted_lihdbr_rate = (row.lihdbr)*conv_rate[conv_rate.length-1]
		  // frappe.model.set_value(row.doctype,row.name,'base_lihdbr',converted_lihdbr_rate)
		  var converted_pr_rate = (row.post_rental_inspection_charges)*conv_rate[conv_rate.length-1]
		  // frappe.model.set_value(row.doctype,row.name,'base_post_rental_inspection_charges',converted_pr_rate)
		  var converted_standby_rate = (row.standby)*conv_rate[conv_rate.length-1]
		  // frappe.model.set_value(row.doctype,row.name,'base_standby',converted_standby_rate)
		  var converted_straight_rate = (row.straight)*conv_rate[conv_rate.length-1]
		  // frappe.model.set_value(row.doctype,row.name,'base_straight',converted_straight_rate)
		  var converted_redress_rate = (row.redress)*conv_rate[conv_rate.length-1]
		  // frappe.model.set_value(row.doctype,row.name,'base_redress',converted_redress_rate)
		  var converted_base_total_amount = (row.total_amount)*conv_rate[conv_rate.length-1]
		  // frappe.model.set_value(row.doctype,row.name,'base_total_amount',converted_base_total_amount)
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

const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 0) {
		get_items_from_supplier_rental_quotation()
	} else if (status == 1) {
		add_sub_rental_receipt()
		add_sub_rental_timesheet()
		add_sub_rental_issue_note()
	}
}

frappe.ui.form.on('Supplier Rental Order Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
	},

	qty(frm, cdt, cdn) {
		calc_total_qty(frm, cdt, cdn)
	},
	get_assets(frm, cdt, cdn) {
		get_assets_to_supplier(frm, cdt, cdn)
	}
});

const get_assets_to_supplier = (frm, cdt, cdn) => {
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
			console.log("asset_list",asset_list)
		    if(asset_list.length){
		    	filters['rental_status'] = "Available For Rent";
		    	filters['item_code'] = row.item_code;
		    	filters['docstatus'] = 1;
		    	filters['name'] = ['not in',asset_list];
		    }
		    else{
		    	filters['rental_status'] = "Available For Rent";
		    	filters['item_code'] = row.item_code;
		    	filters['docstatus'] = 1;
		    }
			return {
				filters: filters
			}
		},
		action(selections) {
			console.log("selections",selections.length)
			
			const cur_row = locals[cdt][cdn]
			console.log("qty",cur_row.qty)
			let serial_nos = ""
			if(selections.length != cur_row.qty){
				frappe.throw(__("Please select same number of assets as the quantity: ")+cur_row.qty)
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


const get_items_from_supplier_rental_quotation = () => {
	const doctype = "Supplier Rental Quotation"
	cur_frm.add_custom_button(doctype, () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: doctype,
			target: this.cur_frm,
			setters: { supplier: cur_frm.doc.supplier, },
			date_field: "date",
			get_query() {
				return {
					filters: {}
				}
			},
			action(selections) {
				if (selections.length > 1) {
					frappe.msgprint(`Please select only single ${doctype} for importing items.`)
					return
				}
				cur_frm.call({
					method: "get_supplier_rental_quotation_items",
					args: {
						docname: selections[0]
					},
					async: false,
					callback(res) {
						const data = res.message
						const cur_doc = cur_frm.doc
						cur_doc.supplier = data.supplier
						cur_doc.supplier_rental_quotation = data.name

						cur_doc.items = []
						for (const row of data.rq_items) {
							let rate = row.rate
							if (data.rate_type == "Per Month") {
								rate = rate / 30
							}

							const new_row = cur_frm.add_child('items', {
								'rate': rate,
								'asset_location': row.asset_location,
								'supplier_rental_quotation': data.name,
							})
							const cdt = new_row.doctype
							const cdn = new_row.name
							frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
							frappe.model.set_value(cdt, cdn, "qty", row.qty)
						}

						cur_frm.refresh()
						cur_dialog.hide()
					}
				})
			}
		});
	}, 'Get Items From')
}

const add_sub_rental_timesheet = () => {
	cur_frm.add_custom_button('Supplier Rental Timesheet', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Supplier Rental Timesheet'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.supplier = doc.supplier
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "supplier_rental_order", doc.name)

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_sub_rental_receipt = () => {
	cur_frm.add_custom_button('Sub Rental Receipt', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Sub Rental Receipt'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.supplier = doc.supplier
				cur_doc.departments = doc.departments
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "sub_rental_order", doc.name)

				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const add_sub_rental_issue_note = () => {
	cur_frm.add_custom_button('Sub Rental Issue', () => {
		const doc = cur_frm.doc
		// frm.clear_table('items');
		frappe.run_serially([
			() => frappe.new_doc('Sub Rental Issue'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.supplier = doc.supplier
				cur_doc.departments = doc.departments
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "sub_rental_order", doc.name)
				cur_frm.refresh()
			}
		])
	}, 'Create')
}

const calc_total_qty = (frm) => {
	let total = 0
	frm.doc.items.map(row => {
		if (row.qty) total += row.qty
	})

	frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total_qty', total)
}


const calculate_lost_and_damage_price = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	const item_code = row.item_code

	frappe.call({
		method: "oil_and_gas_international.events.shared.get_buying_prices",
		args: {
			item_code
		},
		callback(r) {
			const data = r.message
			row.base_operational_running = data[0]
			row.base_standby = data[1]
			row.base_lihdbr = data[2]
			row.base_redress = data[3]
			row.base_straight = data[4]
			row.base_post_rental_inspection_charges = data[5]
			frm.refresh()
		}
	})
	//  convert_base_rate(frm)
}




const calc_days_of_rent = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.from_date && row.to_date) {
		const to_date = new Date(row.to_date)
		const from_date = new Date(row.from_date)
		const difference = Math.floor((to_date - from_date) / (1000 * 60 * 60 * 24) + 1)

		if (difference < 1) {
			frappe.msgprint("To Date can't be before From date!")
			frappe.model.set_value(cdt, cdn, 'days_of_rent', 0)
			return
		}
		frappe.model.set_value(cdt, cdn, 'days_of_rent', difference)
	}
}


const add_material_receipt = () => {
	cur_frm.add_custom_button('Material Receipt', () => {
		const doc = cur_frm.doc
		cur_frm.call({
			method: 'oil_and_gas_international.overriding.check_material_receipt_existence',
			args: {
				"rental_order" : doc.rental_order,
				"sub_rental_order": doc.sub_rental_order,
				"supplier": doc.supplier,
			},
			freeze: true,
			callback: function(r) {
				if(r.message == "False") {
					frappe.run_serially([
						() => frappe.new_doc('Stock Entry'),
						() => {
							const cur_doc = cur_frm.doc
							frappe.model.set_value(cur_doc.doctype,cur_doc.name,"stock_entry_type","Material Receipt")
							frappe.model.set_value(cur_doc.doctype, cur_doc.name, "sub_rental_order", doc.name)
							frappe.model.set_value(cur_doc.doctype, cur_doc.name, "from_supplier", doc.supplier)
							frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.rental_order)
							frappe.model.set_value(cur_doc.doctype, cur_doc.name, "sub_rental_order", doc.name)
			
							cur_doc.items = []
							for (const row of doc.items) {
								const new_row = cur_frm.add_child("items", {
									qty: row.qty,
								})
								const cdt = new_row.doctype
								const cdn = new_row.name
								frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
							}
			
							cur_frm.refresh()
						}
					])
				}
				else{
					frappe.throw(("Material Receipt Already created"))
				}
			}
		});

	}, 'Create')
}


const add_subrental_timesheet = () => {
	cur_frm.add_custom_button('Sub Rental Timesheet', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Supplier Rental Timesheet'),
			() => {
				const cur_doc = cur_frm.doc
				// console.log(typeof doc.start_date)
				cur_doc.customer = doc.customer
				cur_doc.start_date = doc.start_date
				if (doc.end_date){
					cur_doc.end_date = doc.end_date
				}
				else{
					cur_doc.end_date = frappe.datetime.month_end(doc.start_date) 
				}
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				cur_doc.department = doc.department
				cur_doc.division = doc.division
				cur_doc.supplier = doc.supplier
				cur_doc.supplier_rental_order = doc.name
				cur_doc.price_list = "Operational/Running"
				frappe.model.set_value(cur_doc.doctype, cur_doc.name, "rental_order", doc.name)
				cur_doc.items = []
				var no_days = frappe.datetime.get_day_diff(frappe.datetime.month_end(doc.start_date),doc.start_date)+1
				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						qty: row.qty,
						// serial_no_accepted: row.serial_no_accepted,
						operational_running: row.operational_running,
						rate: row.operational_running,
						standby: row.standby,
						post_rental_inspection_charges: row.post_rental_inspection_charges,
						lihdbr: row.lihdbr,
						redress: row.redress,
						straight: row.straight,
						description_2: row.description_2,
						description:row.description,
						customer_requirement: row.customer_requirement,
						delivery_date: doc.start_date,
						days: no_days,
						start_date_: doc.start_date,
						end_date: frappe.datetime.month_end(doc.start_date),

					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
					frappe.model.set_value(cdt, cdn, "item_name", row.item_name)
					frappe.db.get_value("Item", {"item_code": row.item_code}, "stock_uom", (r) => {
						if(r.stock_uom){
							frappe.model.set_value(cdt, cdn, "uom", r.stock_uom)
						}
					});

				}


				cur_frm.refresh()
				cur_frm.refresh()
			}
		])
	}, 'Create')
}
