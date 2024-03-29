// Copyright (c) 2021, Havenir Solutions and contributors
// For license information, please see license.txt

var conv_rate = [1]
frappe.ui.form.on('Rental Quotation', {

	after_workflow_action: function(frm) {
		if (frm.doc.workflow_state == "Rejected"){
			let d = new frappe.ui.Dialog({
				title: 'Reason for Rejection',
				fields: [
					{
						label: 'Reason',
						fieldname: 'reason',
						fieldtype: 'Small Text',
						reqd: 1
					},

				],
				primary_action_label: 'Submit',
				primary_action(values) {
						frm.set_value("sta", values.reason)
						frm.save()
						d.hide();
				}
			});
			
			d.show();
		}
 	 },
	refresh(frm) {
		if (frm.doc.customer){
			frappe.dynamic_link = {doc: frm.doc, fieldname: 'customer', doctype: 'Customer'}
		}
		else if (frm.doc.lead){
			frappe.dynamic_link = {doc: frm.doc, fieldname: 'lead', doctype: 'Lead'}
		}
		create_custom_buttons(frm)
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;
		frm.set_currency_labels([
            "base_operational_running","base_lihdbr","base_post_rental_inspection_charges","base_standby","base_straight","base_redress"
        	], company_currency, "items");
		var customer_currency = frm.doc.currency
		frm.set_currency_labels([
            "operational_running","lihdbr","post_rental_inspection_charges","standby","straight","redress"
        ], customer_currency, "items");
	},
	setup(frm){
		frm.set_query('customer_address',erpnext.queries.address_query)
		frm.set_query('customer_contact',erpnext.queries.contact_query)
		

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
		frm.doc.items.forEach(function(item){
			console.log(item.base_operational_running* frm.doc.conversion_rate)
			if (item.operational_running != 0){
				frappe.model.set_value(item.doctype, item.name, 'base_operational_running', item.operational_running/ frm.doc.conversion_rate);
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
  	},
	terms(frm) {
		if(frm.doc.terms) {
			return frappe.call({
				method: 'erpnext.setup.doctype.terms_and_conditions.terms_and_conditions.get_terms_and_conditions',
				args: {
					template_name: frm.doc.terms,
					doc: frm.doc
				},
				callback: function(r) {
					frm.set_value('terms_and_conditions_details',r.message)
				}
			});
		}
	},
});

const convert_base_rate = function(frm){
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
 //       frappe.model.set_value(row.doctype,row.name,'base_lihdbr',converted_lihdbr_rate)
        var converted_pr_rate = (row.post_rental_inspection_charges)*conv_rate[conv_rate.length-1]
   //     frappe.model.set_value(row.doctype,row.name,'base_post_rental_inspection_charges',converted_pr_rate)
        var converted_standby_rate = (row.standby)*conv_rate[conv_rate.length-1]
     //   frappe.model.set_value(row.doctype,row.name,'base_standby',converted_standby_rate)
        var converted_straight_rate = (row.straight)*conv_rate[conv_rate.length-1]
   //     frappe.model.set_value(row.doctype,row.name,'base_straight',converted_straight_rate)
        var converted_redress_rate = (row.redress)*conv_rate[conv_rate.length-1]
     //   frappe.model.set_value(row.doctype,row.name,'base_redress',converted_redress_rate)
      }
  }
}
// const convert_rate = function(frm){
//   if(frm.doc.items && frm.doc.docstatus!=1){
//     conv_rate.push(frm.doc.conversion_rate)
//       for(let row of frm.doc.items){
//         var converted_op_rate = (row.base_operational_running)*conv_rate[conv_rate.length-1]
//         frappe.model.set_value(row.doctype,row.name,'operational_running',converted_op_rate)
//         var converted_lihdbr_rate = (row.base_lihdbr)*conv_rate[conv_rate.length-1]
//         frappe.model.set_value(row.doctype,row.name,'lihdbr',converted_lihdbr_rate)
//         var converted_pr_rate = (row.base_post_rental_inspection_charges)*conv_rate[conv_rate.length-1]
//         frappe.model.set_value(row.doctype,row.name,'post_rental_inspection_charges',converted_pr_rate)
//         var converted_standby_rate = (row.base_standby)*conv_rate[conv_rate.length-1]
//         frappe.model.set_value(row.doctype,row.name,'standby',converted_standby_rate)
//         var converted_straight_rate = (row.base_straight)*conv_rate[conv_rate.length-1]
//         frappe.model.set_value(row.doctype,row.name,'straight',converted_straight_rate)
//         var converted_redress_rate = (row.base_redress)*conv_rate[conv_rate.length-1]
//         frappe.model.set_value(row.doctype,row.name,'redress',converted_redress_rate)
//       }
//   }
// }

// Rental Quotation Item
frappe.ui.form.on('Rental Quotation Item', {
	item_code(frm, cdt, cdn) {
		calculate_lost_and_damage_price(frm, cdt, cdn)
		const row = locals[cdt][cdn]
		const item_code = row.item_code
		if(!row.description){
		frappe.db.get_value('Item', item_code, ["description"], function(value) {
				frappe.model.set_value(cdt, cdn, "description", value.description);
		});}
	},
	qty(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	rate(frm, cdt, cdn) {
		calc_amount(frm, cdt, cdn)
	},

	amount(frm) {
		calc_total_amount(frm)
	},
	operational_running(frm,cdt,cdn){
		convert_rate(frm)
	},
	lihdbr(frm,cdt,cdn){
		convert_rate(frm)
	},
	post_rental_inspection_charges(frm,cdt,cdn){
		convert_rate(frm)
	},
	standby(frm,cdt,cdn){
		convert_rate(frm)
	},
	straight(frm,cdt,cdn){
		convert_rate(frm)
	},
	redress(frm,cdt,cdn){
		convert_rate(frm)
	},
});

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

// Rental Quotation
const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 0) {
		get_items_from_rental_estimation()
	} else if (status == 1) {
		add_rental_order()
	}
}


const get_items_from_rental_estimation = () => {
	const doctype = "Rental Estimation"
	cur_frm.add_custom_button(doctype, () => {
		new frappe.ui.form.MultiSelectDialog({
			doctype: doctype,
			target: this.cur_frm,
			setters: {
				status: ["in", ["Draft", "Pending Estimation"]],
				customer: cur_frm.doc.customer,
			},
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
					method: "get_rental_estimation_items",
					args: {
						docname: selections[0]
					},
					async: false,
					callback(res) {
						const data = res.message
						const cur_doc = cur_frm.doc
						cur_doc.customer = data.customer
						cur_doc.date = data.date
						cur_doc.valid_till = data.valid_till
						cur_doc.rate_type = data.rate_type
						cur_doc.rental_estimation = data.name

						cur_doc.items = []
						for (const row of data.re_items) {
							const new_row = cur_frm.add_child('items', {
								'qty': row.qty,
								'estimate_rate': row.estimate_rate,
								'asset_location': row.asset_location,
								'rental_estimate': data.name,
								'rental_estimate_item': row.name,
							})
							const cdt = new_row.doctype
							const cdn = new_row.name
							frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
						}

						cur_frm.refresh()
						cur_dialog.hide()
					}
				})

			}
		});
	}, 'Get Items From')
}

const add_rental_order = () => {
	cur_frm.add_custom_button('Rental Order', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Rental Order'),
			() => {				
				const cur_doc = cur_frm.doc
				if (doc.estimation_to == "Lead"){
					frappe.db.get_value("Customer", {"lead_name": doc.lead}, "name", (r) => {
						if(r.name){
							frappe.model.set_value('Rental Order',cur_doc.name,"customer", r.name)
						}
						else{
							frappe.msgprint(__("You need to convert lead to customer First to make the Rental Order"))    
						}
					});
                }
                if (doc.estimation_to == "Customer"){
                    cur_frm.doc.customer = doc.customer;
                    cur_frm.doc.customer_name = doc.customer_name;
                }
				cur_doc.department = doc.departments
				cur_doc.terms = doc.terms
				cur_doc.terms_and_conditions_details = doc.terms_and_conditions_details
				cur_doc.remarks = doc.remarks
				cur_doc.prices = doc.prices
				cur_doc.delivery_terms = doc.delivery_terms
				cur_doc.payment_terms = doc.payment_terms
				cur_doc.freight = doc.freight
				cur_doc.rental_estimation = doc.rental_estimation
				cur_doc.opportunity = doc.opportunity
				cur_doc.currency = doc.currency
				cur_doc.conversion_rate = doc.conversion_rate
				cur_doc.sales_person_link = doc.sales_person
				cur_doc.division = doc.division
				cur_doc.customer_contact = doc.customer_contact
				cur_doc.contact = doc.contact
				cur_doc.customer_address = doc.customer_address
				cur_doc.address = doc.address
                cur_frm.doc.enquery_no = doc.enquery_no
                cur_frm.doc.enquery_ref = doc.enquery_ref
				cur_frm.doc.remarks = doc.remarks
				cur_frm.doc.prices = doc.prices
				cur_frm.doc.delivery_terms = doc.delivery_terms
				cur_frm.doc.validity = doc.validity
				cur_frm.doc.freight = doc.freight_terms
				cur_frm.doc.notes = doc.notes
				cur_frm.doc.credit_limit = doc.credit_limit
				cur_frm.doc.client_terms = doc.client_terms
				cur_frm.doc.company = doc.company

				// frappe.model.set_value('Rental Order', cur_doc.name, "sales_person_link", doc.sales_person)
				frappe.model.set_value('Rental Order', cur_doc.name, "currency", doc.currency)
				frappe.model.set_value('Rental Order', cur_doc.name, "conversion_rate", doc.conversion_rate)
				cur_doc.rental_quotation = doc.name

				cur_doc.items = []
				for (const row of doc.items) {
					let rate = row.rate
					if (doc.rate_type == "Per Month") {
						rate = rate / 30
					}

					const new_row = cur_frm.add_child('items', {
						'description_2': row.description_2,
						'description': row.description,
						'rate': rate,
						'customer_requirement': row.customer_requirement,
						'item_name': row.item_name,
						'rental_quotation': cur_doc.rental_quotation,
						'rental_estimation': cur_doc.rental_estimation,
						'opportunity': cur_doc.opportunity,
						'qty': row.qty,
						'base_operational_running': row.base_operational_running,
						'operational_running': row.base_operational_running* doc.conversion_rate,
						'base_lihdbr': row.base_lihdbr,
						'base_straight': row.base_straight,
						'base_standby': row.base_standby,
						'base_redress': row.base_redress,
						'base_post_rental_inspection_charges' : row.base_post_rental_inspection_charges,
						'lihdbr': row.base_lihdbr* doc.conversion_rate,
						'straight': row.base_straight* doc.conversion_rate,
						'standby': row.base_standby* doc.conversion_rate,
						'redress': row.base_redress* doc.conversion_rate,
						'post_rental_inspection_charges' : row.base_post_rental_inspection_charges* doc.conversion_rate,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
					setTimeout(function() {
						frappe.model.set_value(cdt, cdn, "description", row.description)
						frappe.model.set_value(cdt, cdn, "qty", row.qty)
						frappe.model.set_value(cdt, cdn, "operational_running", row.operational_running)
						frappe.model.set_value(cdt, cdn, "lihdbr", row.lihdbr)
						frappe.model.set_value(cdt, cdn, "standby", row.standby)
						frappe.model.set_value(cdt, cdn, "redress", row.redress)
						frappe.model.set_value(cdt, cdn, "straight", row.straight)
						frappe.model.set_value(cdt, cdn, "post_rental_inspection_charges", row.post_rental_inspection_charges)
					}, 2000);
			}
				cur_frm.refresh()
			}
		])

	}, 'Create')
}

const calc_total_amount = (frm) => {
	let total = 0
	frm.doc.items.map(row => {
		if (row.amount) total += row.amount
	})

	frappe.model.set_value(frm.doc.doctype, frm.doc.name, 'total', total)
}

// Rental Quotation Item
const calculate_lost_and_damage_price = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	const item_code = row.item_code

	frappe.call({
		method: "oil_and_gas_international.events.shared.get_lost_and_damage_prices",
		args: {
			item_code
		},
		callback(r) {
			if (!row.base_operational_running && !row.base_standby && !row.base_lihdbr && !row.base_redress && 
				!row.base_post_rental_inspection_charges){
				const data = r.message
				row.operational_running = data[0]
				row.standby = data[1]
				row.lihdbr = data[2]
				row.redress = data[3]
				row.straight = data[4]
				row.post_rental_inspection_charges = data[5]
				row.base_operational_running = data[0]
				row.base_standby = data[1]
				row.base_lihdbr = data[2]
				row.base_redress = data[3]
				row.base_straight = data[4]
				row.base_post_rental_inspection_charges = data[5]
			}
			frm.refresh()
		}
	})
	convert_base_rate(frm)
}


const calc_amount = (frm, cdt, cdn) => {
	const row = locals[cdt][cdn]
	if (row.qty && row.rate)
		frappe.model.set_value(cdt, cdn, 'amount', row.qty * row.rate)
}