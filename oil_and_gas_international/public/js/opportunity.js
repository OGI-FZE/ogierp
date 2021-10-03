frappe.ui.form.on("Opportunity", {
    setup(frm){
        console.log('working');
        frm.set_query('item_code', 'items', () => {
            return {
                filters: {
                    item_group: 'Products'
                }
            }
        })
    }
})