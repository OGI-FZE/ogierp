// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Contract Review Checklist', {
	onload: function(frm) {
		if(frm.doc.__islocal && !frm.doc.cr_stage_1){
			let queries = ["Are the product requirements defined by the client?","Is this a customer we have done business before?","Does the company have the capability to deliver the product or perform the service required by Customer?",
			"Is the Company having competent people to perform the job?","Are the calibrated measuring and testing equipments available?",
			"Are the delivery requirements acceptable?","Are there any post delivery activities required?","Have all the Legal,statutory/regulatory requirements been determined?"]
			queries.forEach(function (query) {
                let row = frm.add_child('cr_stage_1', {
                    query: query
                });
            });
			cur_frm.refresh_field("cr_stage_1")
			cur_frm.get_field("cr_stage_1").grid.cannot_add_rows = true;
			cur_frm.fields_dict["cr_stage_1"].grid.wrapper.find('.grid-remove-rows').hide();
		}
		if(frm.doc.__islocal && !frm.doc.cr_stage_2){
			let queries = ["Have all the Customer specified requirements been determined?Have terms and conditions been clearly understood /acceptable?",
			"Are there any ambiguities between the quotation and order?",
			"Are the ambiguities resolved?",
			"All the requirement have been identified and documented to proceed with customer Purchase Order",
			"Is MOC applicable for this job?",
			"Is Risk assessment & contingency plans available for this job?",
			"Is API Monogram required for this job?",
			"Design & Development Requirements?",
			"Is there any other requirements not stated by the customer but essential for this contract?"]
			queries.forEach(function (query) {
                let row = frm.add_child('cr_stage_2', {
                    query: query
                });
            });
			cur_frm.refresh_field("cr_stage_2")
			cur_frm.get_field("cr_stage_2").grid.cannot_add_rows = true;
			cur_frm.fields_dict["cr_stage_2"].grid.wrapper.find('.grid-remove-rows').hide();
		}
		if(frm.doc.__islocal && !frm.doc.cr_stage_2a){
			let queries = ["NDT Requirements (LPT, MPI, UT & RT)",
			"Out source activity (Machining, Machining of Premium Connections)",
			"Coating Requirement",
			"Abbrasive Blasting Requirements",
			"Engineering Drawings / Quality Plan Approval from Client",
			"TPI / Client Witness"]
			queries.forEach(function (query) {
                let row = frm.add_child('cr_stage_2a', {
                    query: query
                });
            });
			cur_frm.refresh_field("cr_stage_2a")
			cur_frm.get_field("cr_stage_2a").grid.cannot_add_rows = true;
			cur_frm.fields_dict["cr_stage_2a"].grid.wrapper.find('.grid-remove-rows').hide();
		}
		if(frm.doc.__islocal && !frm.doc.cr_stage_3){
			let queries = ["Are the requirements in the amendment reviewed?",
			"Are the changes in requirements communicated to the concerned personnel?"]
			queries.forEach(function (query) {
                let row = frm.add_child('cr_stage_3', {
                    query: query
                });
            });
			cur_frm.refresh_field("cr_stage_3")
			cur_frm.get_field("cr_stage_3").grid.cannot_add_rows = true;
			cur_frm.fields_dict["cr_stage_3"].grid.wrapper.find('.grid-remove-rows').hide();
		}
	}
});