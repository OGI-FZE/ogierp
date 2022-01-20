frappe.ui.form.on("Sales Invoice", {
    refresh(frm,cdt,cdn) {
        frm.fields_dict["items"].grid.add_custom_button(__('Fetch Timesheet Amount'), 
			function() {
				rate_calc(frm);
        });
        frm.fields_dict["items"].grid.grid_buttons.find('.btn-custom').removeClass('btn-default').addClass('btn-primary');
        
    },
    rental_timesheet(frm, cdt, cdn) {
        if(frm.doc.rental_timesheet){
		    get_items_from_rental_timesheet(frm, cdt, cdn)
        }
	},

})


const get_items_from_rental_timesheet = (frm, cdt, cdn) => {
	const rental_timesheet = frm.doc.rental_timesheet
	frappe.call({
		method: "oil_and_gas_international.events.sales_invoice.get_rental_timesheet_items",
		args: { docname: rental_timesheet },
		async: false,
		callback(res) {
			const data = res.message
			if (!data) return
			frm.doc.items = []
			for (const row of data) {
                const new_row = cur_frm.add_child("items", {
                    qty: 1,
                    asset_item:row.item_code,
                    rental_order:row.rental_order,
                    rental_order_item:row.rental_order_item,
                })
                const cdt = new_row.doctype
                const cdn = new_row.name
                frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
                setTimeout(function(){
                    frappe.model.set_value(cdt, cdn, "price_list_rate",row.amount)
                    frappe.model.set_value(cdt, cdn, "rate",row.amount)
                    frappe.model.set_value(cdt, cdn, "amount",row.amount)
                }, 2000);           
				
			}

			cur_frm.refresh()
		}
	})
}

const rate_calc=(frm)=>{
    if(!frm.doc.rental_timesheet){
        frappe.msgprint('Please select a Rental Timesheet')
        return
    }   
    frappe.call({
        method: "oil_and_gas_international.events.sales_invoice.get_retal_order_rate",
        async:false,
        args: {
            si_items: frm.doc.items,
            timesheet:frm.doc.rental_timesheet
        },
        callback(r) {
            for(let row of zip(frm.doc.items,r.message)){ 
                let cdt=row[0].doctype;
                let cdn=row[0].name;
                setTimeout(() => {
                    frappe.model.set_value(cdt, cdn, "price_list_rate", row[1].amount)
                    frappe.model.set_value(cdt, cdn, "rate", row[1].amount)
                }, 1000);
            }
            
        }
    })
    
}
const zip = (a, b) => a.map((k, i) => [k, b[i]]);