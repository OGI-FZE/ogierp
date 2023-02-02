
frappe.ui.form.on('Quotation', {
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
						frm.set_value("reason_for_rejection", values.reason)
						frm.save()
						d.hide();
				}
			});
			
			d.show();
		}
 	},
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