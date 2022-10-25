// Copyright (c) 2022, Havenir Solutions and contributors
// For license information, please see license.txt

frappe.ui.form.on('Estimation Sheet', {
	refresh: function(frm) {
		cur_frm.get_field("items").grid.cannot_add_rows = true;
		cur_frm.get_field("items").grid.only_sortable();
		if(frm.doc.docstatus == 1) {
			cur_frm.add_custom_button(__('Quotation'), () => {
				frappe.model.open_mapped_doc({
					method: "oil_and_gas_international.oil_and_gas_international.doctype.estimation_sheet.estimation_sheet.make_quotation",
					frm: cur_frm
				})
			}, __('Create'));
		}
	},
	onload: function(frm) {
		cur_frm.get_field("items").grid.cannot_add_rows = true;
		cur_frm.get_field("items").grid.only_sortable();
	},
});

frappe.ui.form.on('Estimation Sheet Item', {
	qty(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	raw_material_cost(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	cutting_charges(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	od_id_profiling(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	machining_connection_1(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	machining_connection_2(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	marking(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	phosphating(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	other_operational_cost(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	consumables(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	panting(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	packing(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	logistics(frm, cdt, cdn) {
		calc_total_cost(frm, cdt, cdn)
	},
	items_remove: function(frm,cdt,cdn){
		calc_total_cost(frm, cdt, cdn)
	},

});

const calc_total_cost = (frm,cdt,cdn) => {
	console.log("calc_total_cost")
	let total = 0
	let unit = 0
	frm.doc.items.map(row => {
		unit += flt(row.raw_material_cost) + flt(row.cutting_charges) + flt(row.od_id_profiling) + flt(row.machining_connection_1) + flt(row.machining_connection_2) +
				flt(row.marking) + flt(row.phosphating) + flt(row.other_operational_cost) + flt(row.consumables) + flt(row.panting) + flt(row.packing) + flt(row.logistics)
		if (row.qty) total += (row.qty * unit)
	})
	frappe.model.set_value(cdt, cdn, 'unit_cost', unit)
	frappe.model.set_value(cdt, cdn, 'total_cost', total)
}