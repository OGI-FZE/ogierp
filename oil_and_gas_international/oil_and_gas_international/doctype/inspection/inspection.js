// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inspection',"onload", function(frm) {
	
	if (frm.doc.work_order & frm.doc.docstatus == 0){
		frappe.db.get_value("Work Order",{'name':frm.doc.work_order}, ["pending_to_inspect"], (r) => {
			if (r.pending_to_inspect){
				
				console.log(r.pending_to_inspect)
				frm.set_value("pending_quantity", r.pending_to_inspect)
			}
		})
	}

	frm.fields_dict['drill_collar_parameters'].grid.get_field('serial_no').get_query =
			function(doc, cdt, cdn) {
        		var child = locals[cdt][cdn];
				return {
					filters: {
              		  'item_code': doc.item_code,
					  'status': "Active",
					  "warehouse": doc.warehouse

				}
				}
			}
	frm.fields_dict['tubing_parameters'].grid.get_field('serial_no').get_query =
			function(doc, cdt, cdn) {
        		var child = locals[cdt][cdn];
				return {
					filters: {
              		  'item_code': doc.item_code,
					  'status': "Active",
					  "warehouse": doc.warehouse

				}
				}
			}
	frm.fields_dict['drilling_tools_parameters'].grid.get_field('serial_no').get_query =
		function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
					'item_code': doc.item_code,
				'status': "Active",
				"warehouse": doc.warehouse

			}
			}
		}
	frm.fields_dict['heavy_weight_drill_pipe_parameters'].grid.get_field('serial_no').get_query =
		function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
					'item_code': doc.item_code,
					'status': "Active",
					"warehouse": doc.warehouse

			}
			}
		}
	frm.fields_dict['near_stabilizer_parameters'].grid.get_field('serial_no').get_query =
		function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
					'item_code': doc.item_code,
					'status': "Active",
					"warehouse": doc.warehouse

			}
			}
		}
	frm.fields_dict['drill_pipe_parameters'].grid.get_field('serial_no').get_query =
		function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
					'item_code': doc.item_code,
					'status': "Active",
					"warehouse": doc.warehouse
			}
			}
		}

	frm.fields_dict['string_stabilizer_parameters'].grid.get_field('serial_no').get_query =
		function(doc, cdt, cdn) {
			var child = locals[cdt][cdn];
			return {
				filters: {
					'item_code': doc.item_code,
					'status': "Active",
					"warehouse": doc.warehouse
			}
			}
		}
});


frappe.ui.form.on("Inspection", {
    on_submit(frm) {
		if (frm.doc.work_order){
		frm.call({
			method: 'oil_and_gas_international.oil_and_gas_international.doctype.inspection.inspection.change_wo_qty',
			args: {
				"work_order" : frm.doc.work_order,
				"total_inspected_for_order": frm.doc.total_inspected_for_order,
				"total_inspected": frm.doc.total_inspected
			},
			freeze: true,
			callback: function(r) {
				if(!r.message) {
					console.log(" ")
			}
		}
		});	
	}
	},

	warehouse(frm){
		if (!frm.doc.work_order & frm.doc.docstatus == 0){
			frappe.db.get_value("Bin",{'warehouse':frm.doc.warehouse,'item_code':frm.doc.item_code}, ["actual_qty"], (r) => {
				if (r.actual_qty){
					frm.set_value("pending_quantity", r.actual_qty)
				}
			})
		}
	}
	
})
