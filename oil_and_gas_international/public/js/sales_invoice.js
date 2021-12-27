frappe.ui.form.on("Sales Invoice", {
    refresh(frm) {
        create_custom_buttons(frm)
        
    },
    onload: function (frm, cdt, cdn) {
        let btn = document.createElement('a');
        btn.innerText = 'Fetch Rates';
        btn.className = 'grid-upload btn btn-xs btn-default';
        frm.fields_dict.items.grid.wrapper.find('.grid-upload').removeClass('hide').parent().append(btn);
        btn.addEventListener("click", function(){
            rate_calc(frm);
        });
    },	
    validate:function(frm){
        if(frm.doc.rental_order){
            frappe.db.get_doc('Rental Order',frm.doc.rental_order )
            .then(doc => {
                for(let row of doc.items){
                    for(let item of frm.doc.items){
                        if(row.item_code==item.asset_item){
                            const cdt=item.doctype;
                            const cdn=item.name;
                            frappe.model.set_value(cdt,cdn,'rate',row.total_amount)
                        }
                    }   
                }
            })
        }
    }
})



const create_custom_buttons = (frm) => {
    frm.add_custom_button("Fetch Rental Order", () => {
        if (!frm.doc.customer) {
            frappe.throw("Please select customer!")
        }

        const doctype = "Rental Order"
        new frappe.ui.form.MultiSelectDialog({
            doctype: doctype,
            target: this.cur_frm,
            setters: {},
            date_field: "date",
            get_query() {
                return {
                    filters: {
                        docstatus: 1,
                        customer: frm.doc.customer
                    }
                }
            },
            action(selections) {
                frappe.call({
                    method: "oil_and_gas_international.events.sales_invoice.get_rental_order_items",
                    async:false,
                    args: {
                        rental_orders: selections
                    },
                    callback(r) {
                        frm.doc.items = []
                        const data = r.message
                        for (const row of data) {
                            const new_row = frm.add_child("items", {
                                "rental_order": row.parent,
                                "rental_order_item": row.name,
                                "rental_timesheet": row.parent,
                                "rental_timesheet_item": row.name,
                            })

                            const cdt = new_row.doctype
                            const cdn = new_row.name
                            frappe.model.set_value(cdt, cdn, "item_code", 'Asset Rent Item')
                            frappe.model.set_value(cdt, cdn, "asset_item", row.item_code)
                            frappe.model.set_value(cdt, cdn, "qty", 1)
                            frappe.model.set_value(cdt, cdn, "rental order_item", row.name)
                            setTimeout(() => {
                                if(!row.billed_amount){
                                    frappe.model.set_value(cdt, cdn, "rate", row.total_amount)
                                }else{
                                    frappe.model.set_value(cdt, cdn, "rate", row.total_amount-row.billed_amount)
                                }
                            }, 5000);
                        }

                        frm.refresh_field("items")
                        cur_dialog.hide()
                    }
                })
            }
        });
    })
    
}
const rate_calc=(frm)=>{
    frappe.call({
        method: "oil_and_gas_international.events.sales_invoice.get_retal_order_rate",
        async:false,
        args: {
            si_items: frm.doc.items
        },
        callback(r) {
            for(let row of zip(frm.doc.items,r.message)){ 
                let cdt=row[0].doctype
                let cdn=row[0].name
                ;

                if(row[0].rental_order_item){
                    setTimeout(() => {
                        if(!row[1].billed){
                            frappe.model.set_value(cdt, cdn, "price_list_rate", row[1].total)
                        }else{
                            frappe.model.set_value(cdt, cdn, "price_list_rate", row[1].total-row[1].billed)
                        }
                    }, 1000);
                }
                
            }
            
        }
    })
    
}
const zip = (a, b) => a.map((k, i) => [k, b[i]]);