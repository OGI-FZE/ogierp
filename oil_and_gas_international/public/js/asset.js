frappe.ui.form.on("Asset", {
    refresh(frm) {
        if (frm.doc.rental_status == "On hold for Inspection") {
            create_custom_buttons(frm)
        }
        if (frm.doc.rental_status == "Delivered to supplier") {
            if(frm.doc.is_sub_rental_asset){
                create_sub_custom_button(frm)
            }
        }
        if(!frm.doc.__islocal) {
            frm.add_custom_button(__('Asset Utilization'), function () {
                frappe.set_route('query-report', 'Asset Utilization Report', {asset:frm.doc.name});
            }, __('View'));
        }
    },
    validate(frm) {
        if(frm.doc.purchase_receipt){
            frappe.db.get_value('Purchase Receipt', frm.doc.purchase_receipt, "supplier", function(value) {
                frappe.model.set_value('Asset',frm.doc.name,'supplier_info',value['supplier'])
            });
        }
        if(frm.doc.purchase_invoice){
            frappe.db.get_value('Purchase Invoice', frm.doc.purchase_invoice, "supplier", function(value) {
                frappe.model.set_value('Asset',frm.doc.name,'supplier_info',value['supplier'])
            });
        }
    },
    status(frm) {
        if(frm.doc.status){
            if(frm.doc.status in ['Sold','Scrapped','In Maintenance','Out of Order']){
                frappe.model.set_value('Asset',frm.doc.name,'rental_status',frm.doc.status)
            }
        }
    },
    is_sub_rental_asset(frm){
        if(frm.doc.is_sub_rental_asset){
            frappe.model.set_value('Asset',frm.doc.name,'rental_status',"Sub Rental Asset")
        }
        else{
            frappe.model.set_value('Asset',frm.doc.name,'rental_status',"Available for Rent")
        }
    }
})


const create_custom_buttons = (frm) => {
    frm.add_custom_button("Available for Rent", (frm) => {
        cur_frm.set_value("rental_status", "Available for Rent")
        cur_frm.savesubmit()
    }) 
}

const create_sub_custom_button = (frm) => {
    frm.add_custom_button("Sub Rental Asset", (frm) => {
        cur_frm.set_value("rental_status", "Sub Rental Asset")
        cur_frm.savesubmit()
    })
}