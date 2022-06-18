frappe.ui.form.on('Project', {
	after_save(frm){
		if(frm.doc.rental_order){
			frappe.db.set_value("Rental Order", frm.doc.rental_order, "project",frm.doc.name);
		}
	}
});