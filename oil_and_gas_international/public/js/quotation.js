
frappe.ui.form.on('Quotation', {
	onload: function(frm) {
		console.log("onload")
		if (frm.doc.__islocal && frm.doc.opportunity){
			console.log("new one with opportunity")
			frappe.call({
				method: "oil_and_gas_international.events.shared.get_estimation",
				args: {
					opp : frm.doc.opportunity
				},
				callback(r) {
					if(r.message){
						frm.set_value('estimation_sheet', r.message);
					}
				}
			})
		}
	}
});