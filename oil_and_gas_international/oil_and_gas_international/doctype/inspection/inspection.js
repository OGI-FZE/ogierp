// Copyright (c) 2023, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Inspection',"onload", function(frm) {
	frm.fields_dict['drill_collar_parameters'].grid.get_field('serial_no').get_query =
			function(doc, cdt, cdn) {
        		var child = locals[cdt][cdn];
				return {
					filters: {
              		  'item_code': doc.item_code,
				}
				}
			}
	
});




