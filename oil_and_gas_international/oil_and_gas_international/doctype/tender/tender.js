// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Tender', {
	refresh(frm){
		create_custom_buttons()
	}

});

const create_custom_buttons = () => {
	const doc = cur_frm.doc
	const status = doc.docstatus

	if (status == 1) {
		add_tender_review()
	}
}

const add_tender_review = () => {
	cur_frm.add_custom_button('Tender Review Chceklist', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('Tender Review Checklist'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.customer = doc.customer
				cur_doc.tender_no = doc.name
				cur_doc.division = doc.division
				cur_doc.date = doc.date




				cur_frm.refresh()
			}
		
		])
	}, 'Create')
}