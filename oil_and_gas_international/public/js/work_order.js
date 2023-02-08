frappe.ui.form.on('Work Order', {
	onload(frm) {
        if (frm.rental_order || frm.sales_order){
            frm.set_df_property('division', 'read_only', 1);
        }
    }

	
});
