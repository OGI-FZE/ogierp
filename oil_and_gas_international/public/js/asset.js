frappe.ui.form.on("Asset", {
    setup: function(frm) {
        frm.fields_dict.tubulars.grid.get_field('asset').get_query = function(doc, cdt, cdn) {
        var child = locals[cdt][cdn];
        return {  
          filters:[
            ['is_string_asset', '=', 0],
            ['docstatus', '=', 1],
            ['rental_status', '=', "Available for Rent"]
          ]
        };
      }; 
    },
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
    },
    // remove_assets(frm) {
    //     remove_assets_from_tubulars(frm)
    // }
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

const remove_assets_from_tubulars = (frm) => {
    console.log("remove_assets_from_tubulars")
    new frappe.ui.form.MultiSelectDialog ({
        doctype: "Asset",
        target: this.cur_frm,
        setters: {
            asset_name: null
        },
        get_query() {
            let asset_list = []
            let filters = {};
            $.each(frm.doc.tubulars, function(_idx, val) {
                if (val.asset) asset_list.push(val.asset);
            });
            filters['name'] = ['in',asset_list];
            filters['docstatus'] = 1;
            return {
                filters: filters
            }
        },
        action(selections) {
            for (var i = 0; i < frm.doc.tubulars.length; i++) {
                if(frm.doc.tubulars[i] in selections) {
                    frm.get_field("suppliers").grid.grid_rows[i].remove();
                }
            }
        }
    })
}

frappe.ui.form.on('Tubulars', {
    before_tubulars_remove:function (frm, cdt, cdn) {
    let row = frappe.get_doc(cdt, cdn);
    if(row.asset){
        frappe.db.get_doc("Asset", row.asset)
            .then((doc) => {
                frappe.db.set_value('Asset',doc.name,'rental_status',"On hold for Inspection")
                frappe.call({
                    method: 'oil_and_gas_international.events.asset.set_initial_location',
                    args: {
                        asset: doc.name,
                    },
                    callback: function(r) {
                        console.log("r",r.message)
                        // frappe.db.set_value('Asset',doc.name,'location',r.message)
                    }
                }); 
            });   
        }
    }
})


