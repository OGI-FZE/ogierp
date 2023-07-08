frappe.ui.form.on('Stock Entry', {
	refresh(frm) {
        create_custom_buttons(frm)
        // if (frm.doc.return_from_rent && frm.doc.docstatus == 1){
        //     create_inspection(frm)
        // }
    }
});


const create_inspection = (frm) => {
	cur_frm.add_custom_button('Inspect Returned Items', () =>{
        for (const row of frm.doc.items){
            frappe.call({
                method: 'oil_and_gas_international.overriding.inspect_returned_serial_no',
                args: {
                    ro: frm.doc.rental_order,
                    item_code: row.item_code,
                    stock_entry: frm.doc.stock_entry,
                    serial_no: row.serial_no

                },
                callback: function(r) {
                    console.log("done")
    
                }
            });
        }

    })
}

frappe.ui.form.on('Stock Entry Detail', {
	item_code(frm,cdt,cdn) {
        const item = locals[cdt][cdn]
        const args = {
            'item_code'			: item.item_code,
            'posting_date'		: frm.doc.posting_date,
            'posting_time'		: frm.doc.posting_time,
            'warehouse'			: cstr(item.s_warehouse) || cstr(item.t_warehouse),
            'serial_no'			: item.serial_no,
            'company'			: frm.doc.company,
            'qty'				: item.s_warehouse ? -1*flt(item.transfer_qty) : flt(item.transfer_qty),
            'voucher_type'		: frm.doc.doctype,
            'voucher_no'		: item.name,
            'allow_zero_valuation': 1,
        };
        frappe.call({
            method: "erpnext.stock.utils.get_incoming_rate",
            args: {
                args: args
            },
            callback: function(r) {
                frappe.model.set_value(cdt, cdn, 'customer_rate', (r.message || 0.0));
                // frappe.model.set_value(cdt, cdn, "customer_amount", item.customer_rate* item.qty)
                frm.events.calculate_basic_amount(frm, item);
            }
        });
	},

    qty(frm,cdt,cdn) {
        const item = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'customer_amount', item.qty*item.customer_rate);
	},
    customer_rate(frm,cdt,cdn) {
        const item = locals[cdt][cdn]
        frappe.model.set_value(cdt, cdn, 'customer_amount', item.qty*item.customer_rate);
	},

})



const add_packing_slip = () => {
	cur_frm.add_custom_button('Packing Slip', () => {
		const doc = cur_frm.doc
		frappe.run_serially([
			() => frappe.new_doc('OGI Packing Slip'),
			() => {
				const cur_doc = cur_frm.doc
				cur_doc.items = []
                cur_doc.stock_entry = doc.name
				for (const row of doc.items) {
					const new_row = cur_frm.add_child("items", {
						item_code: row.item_code,
						// serial_no_accepted: row.serial_no_accepted,
						qty: row.qty,
					})
					const cdt = new_row.doctype
					const cdn = new_row.name
					frappe.model.set_value(cdt, cdn, "item_code", row.item_code)
					frappe.model.set_value(cdt, cdn, "item_name", row.item_name)

				}


				cur_frm.refresh()
				cur_frm.refresh()
			}
		])
	}, 'Create')
}



const create_custom_buttons = () => {
    const doc = cur_frm.doc
    if (doc.status != 0){
        add_packing_slip()
    }
}



