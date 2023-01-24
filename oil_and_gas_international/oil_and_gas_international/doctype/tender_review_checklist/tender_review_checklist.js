frappe.ui.form.on('Tender Review Checklist', {
	onload: function(frm) {
		if(frm.doc.__islocal && !frm.doc.terms){
			let queries = ["Read the ITT completely","Understand the requirement","Check with Management /tender committee for the below points",
			"Detailed scope of work","Suppliers who can help","Contract duration","Contract Termination",
			"Delivery terms that is mentioned in ITT and what we are offering","Payment terms that is mentioned in ITT and what we are offering",
			"Transportation cost bearing that is mentioned in ITT and what we are offering","Training to the personnel’s if any that is mentioned in ITT and what we are offering",
			"Bid bonds if any that is mentioned in ITT and what we are offering","Currencies and the mark up",
			"Customs duty bearing and other clearance formalities that is mentioned in ITT and what we are offering",
			"Taxes and other security deposits if any","Liquidating damages if any that is mentioned in ITT","Exemptions suggested by management",
			"Evaluation criteria stated in ITT","Format of submission – hard copy or soft copy","Guarantee/warranty and any other legal terms that is not in favor of OGI",
			"Pricing format to be submitted as per ITT or OGI format is fine","Standard documents to be submitted","Index – Technical and commercial",
			"Cover letters","Manuals","Technical unpriced offer, relevant experience, client list etc","OGI profile and brochure","Licenses and insurances and other requested documents",
			"QHSE and QMS documents","Personnel profile and CV","Labels for submission","Other documents requested in RFQ if any","Financial documents",
			"Organograms, method statement, form of contract etc"]
			queries.forEach(function (query) {
                let row = frm.add_child('terms', {
                    query: query
                });
            });
			cur_frm.refresh_field("terms")
			cur_frm.get_field("terms").grid.cannot_add_rows = true;
			cur_frm.fields_dict["terms"].grid.wrapper.find('.grid-remove-rows').hide();
		}
	}
});