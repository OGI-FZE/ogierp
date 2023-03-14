frappe.ui.form.on('Stock Entry', {
	refresh(frm) {
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




