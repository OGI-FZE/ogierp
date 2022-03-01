frappe.ui.form.on('Purchase Invoice', {
	rental_order(frm) {
		if(frm.doc.rental_order){
			set_project(frm)
		}
	}
});

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