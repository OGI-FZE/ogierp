frappe.ui.form.on('Packing Slip', {
    add_to_detail(frm) {
		var ids = ""
		frm.refresh_field('items')
	    var selected = {items: frm.fields_dict.items.grid.get_selected_children()};
		console.log(typeof(selected))
		for (const idx of selected.items){
            if (ids == ""){
                ids = "Items " + idx.idx
            }
            else{
                ids = ids + "," + idx.idx
            }
		}
		console.log(selected.items)
		console.log(ids)
		frm.add_child("packing_details",{
			"packing_details":ids
		})
		frm.refresh_field("packing_details")

    }
});

