frappe.ui.form.on("Budget Details", {
    rate: function(frm, cdt, cdn){
        cal_amount(frm, cdt, cdn)
    },
    quantity: function(frm, cdt, cdn){
        cal_amount(frm, cdt, cdn)
    }
})

var cal_amount = function(frm,cdt, cdn){
    let row = locals[cdt][cdn]
    if (row .quantity && row .rate){
        let amount = row .quantity * row .rate
        frappe.model.set_value(cdt, cdn, "amount",amount)
    }
    else {
        frappe.model.set_value(cdt, cdn, "amount", 0)
    }
}