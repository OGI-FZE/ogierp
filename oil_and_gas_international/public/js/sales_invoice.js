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
            set_project(frm)
        }
	},

});


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
                    days:row.days,
                    asset_qty:row.qty
                })
                const cdt = new_row.doctype
                const cdn = new_row.name
                frappe.model.set_value(cdt, cdn, "item_code",'Asset Rent Item')
                
                let desc = ""
                if(row.item_code) {desc += row.item_name+"\n"}
                if(row.operational_running_days){
                    desc += "Operational/Running  " 
                    frappe.model.set_value(cdt, cdn, "unit_price",row.operational_running)
                }
                if(row.standby_days){
                    desc += "Standby  "
                    frappe.model.set_value(cdt, cdn, "unit_price",row.standby)
                }
                if(row.straight_days){
                    desc += "Straight  "
                    frappe.model.set_value(cdt, cdn, "unit_price",row.straight)
                }
                if(row.timesheet_start_date && row.timesheet_end_date) {desc += ("\nRental period: "+ row.timesheet_start_date +" to "+row.timesheet_end_date)}
               
                setTimeout(function(){
                    frappe.model.set_value(cdt, cdn, "price_list_rate",row.amount)
                    frappe.model.set_value(cdt, cdn, "rate",row.amount)
                    frappe.model.set_value(cdt, cdn, "amount",row.amount)
                    frappe.model.set_value(cdt, cdn, "days",row.days)
                    frappe.model.set_value(cdt, cdn, "child_category",row.item_group)
                    frappe.model.set_value(cdt, cdn, "details",desc)
                    frappe.model.set_value(cdt, cdn, "description",desc)
                }, 2000);           
				
			}

			cur_frm.refresh()
		}
	})
}

const set_project = (frm) => {
    frappe.db.get_value('Rental Timesheet', {'name':frm.doc.rental_timesheet}, 'rental_order', (r) => {
        if(r && r.rental_order){
            const rental_order = r.rental_order
            frm.call({
                method: "oil_and_gas_international.oil_and_gas_international.doctype.rental_issue_note.rental_issue_note.get_project",
                args: { docname: rental_order },
                async: false,
                callback(res){
                    console.log(res)
                    const data = res.message
                    frm.set_value("project", data.name)
                }
            })
        }
        
    });
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
