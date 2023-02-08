from frappe.model.document import Document, _
import frappe


class Inspection(Document):
	def validate(self):
		i = self.item_code
		warehouse_qty = frappe.db.get_value("Bin",{"item_code":self.item_code,"warehouse":self.warehouse},"actual_qty")
		if not warehouse_qty:
			warehouse_qty = 0

		parameters = [self.drill_collar_parameters,
					  self.heavy_weight_drill_pipe_parameters,
					  self.drill_pipe_parameters,
					  self.tubing_parameters,
					  self.near_stabilizer_parameters,
					  self.string_stabilizer_parameters,
					  self.drilling_tools_parameters]
		for parameter in parameters:
			if parameter and parameter == self.drill_collar_parameters:
					if float(warehouse_qty) < len(parameter):
						frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
					for serial_no in self.drill_collar_parameters:
						conditions = [not get_q_i_t_p(i,"length")['min_value'] <= serial_no.length <= get_q_i_t_p(i,"length")['max_value'] or
								not get_q_i_t_p(i,"OD")['min_value'] <= float(serial_no.od) <= get_q_i_t_p(i,"OD")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"SRG Dia")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"SRG Dia")['max_value'] or
								not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"SRG Width")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"SRG Width")['max_value'] or
								not get_q_i_t_p(i,"Neck Length")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"Neck Length")['max_value'] or
								not get_q_i_t_p(i,"Pin Tong Space")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"Pin Tong Space")['max_value'] or
								not get_q_i_t_p(i,"MPI Connection")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"MPI Connection")['max_value'] or
								not get_q_i_t_p(i,"Condition")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"Condition")['max_value'] 
								]
						if conditions[0]:
							serial_no.status= "Failed"
						else: 
							serial_no.status= "Validated"

			elif parameter and parameter == self.heavy_weight_drill_pipe_parameters:
				if float(warehouse_qty) < len(parameter):
					frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
				for serial_no in self.heavy_weight_drill_pipe_parameters:
					conditions = [not get_q_i_t_p(i,"length")['min_value'] <= serial_no.length <= get_q_i_t_p(i,"length")['max_value'] or
							not get_q_i_t_p(i,"OD")['min_value'] <= float(serial_no.od) <= get_q_i_t_p(i,"OD")['max_value'] or
							not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
							not get_q_i_t_p(i,"Tube Condition")['min_value'] <= float(serial_no.tube_condition) <= get_q_i_t_p(i,"Tube Condition")['max_value'] or
							not get_q_i_t_p(i,"Internal Coating")['min_value'] <= float(serial_no.internal_coating) <= get_q_i_t_p(i,"Internal Coating")['max_value'] or
							not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= float(serial_no.bevel_dia) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
							not get_q_i_t_p(i,"SRG Dia")['min_value'] <= float(serial_no.srg_dia) <= get_q_i_t_p(i,"SRG Dia")['max_value'] or
							not get_q_i_t_p(i,"SRG Width")['min_value'] <= float(serial_no.srg_width) <= get_q_i_t_p(i,"SRG Width")['max_value'] or
							not get_q_i_t_p(i,"Pin Nose Dia")['min_value'] <= float(serial_no.pin_nose_dia) <= get_q_i_t_p(i,"Pin Nose Dia")['max_value'] or
							not get_q_i_t_p(i,"Pin Cyl. Dia")['min_value'] <= float(serial_no.pin_cyl_dia) <= get_q_i_t_p(i,"Pin Cyl. Dia")['max_value'] or
							not get_q_i_t_p(i,"Pin Tong Space")['min_value'] <= float(serial_no.pin_tong_space) <= get_q_i_t_p(i,"Pin Tong Space")['max_value'] or
							not get_q_i_t_p(i,"Hardband Condition")['min_value'] <= float(serial_no.hardband_condition) <= get_q_i_t_p(i,"Hardband Condition")['max_value'] or
							not get_q_i_t_p(i,"MPI Connection")['min_value'] <= float(serial_no.mpi_connection) <= get_q_i_t_p(i,"MPI Connection")['max_value'] or
							not get_q_i_t_p(i,"Condition")['min_value'] <= float(serial_no.condition) <= get_q_i_t_p(i,"Condition")['max_value'] or
							not get_q_i_t_p(i,"Slip/Upset Area Condition")['min_value'] <= float(serial_no.slipupset_area_condition) <= get_q_i_t_p(i,"Slip/Upset Area Condition")['max_value'] 
							]
					if conditions[0]:
						serial_no.status= "Failed"
					else: 
						serial_no.status= "Validated"
			elif parameter and parameter == self.drill_pipe_parameters:
					if float(warehouse_qty) < len(parameter):
						frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
					for serial_no in self.drill_pipe_parameters:
						conditions = [not get_q_i_t_p(i,"length")['min_value'] <= serial_no.length <= get_q_i_t_p(i,"length")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"OD Conditions/STNS")['min_value'] <= float(serial_no.od_conditions_stns) <= get_q_i_t_p(i,"OD Conditions/STNS")['max_value'] or
								not get_q_i_t_p(i,"Remaining Wall Thickness")['min_value'] <= float(serial_no.remaining_wall_thickness) <= get_q_i_t_p(i,"Remaining Wall Thickness")['max_value'] or
								not get_q_i_t_p(i,"Internal Coating")['min_value'] <= float(serial_no.internal_coating) <= get_q_i_t_p(i,"Internal Coating")['max_value'] or
								not get_q_i_t_p(i,"EMI")['min_value'] <= float(serial_no.emi) <= get_q_i_t_p(i,"EMI")['max_value'] or
								not get_q_i_t_p(i,"Pin Connection Length")['min_value'] <= float(serial_no.pin_connection_length) <= get_q_i_t_p(i,"Pin Connection Length")['max_value'] or
								not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= float(serial_no.bevel_dia) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"Pin Tong Space")['min_value'] <= float(serial_no.tong_space) <= get_q_i_t_p(i,"Pin Tong Space")['max_value'] or
								not get_q_i_t_p(i,"Pin Lead")['min_value'] <= float(serial_no.pin_lead) <= get_q_i_t_p(i,"Pin Lead")['max_value'] 
								]
						if conditions[0]:
							serial_no.status= "Failed"
						else: 
							serial_no.status= "Validated"
			elif parameter and parameter == self.tubing_parameters:
					if float(warehouse_qty) < len(parameter):
						frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
					for serial_no in self.tubing_parameters:
						conditions = [not get_q_i_t_p(i,"length")['min_value'] <= serial_no.length <= get_q_i_t_p(i,"length")['max_value'] or
								not get_q_i_t_p(i,"Specification")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= float(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] 
 
								]
						if conditions[0]:
							serial_no.status= "Failed"
						else: 
							serial_no.status= "Validated"


	def on_submit(self):
		accepted_sn = []
		parameters = [self.drill_collar_parameters,
					  self.heavy_weight_drill_pipe_parameters,
					  self.drill_pipe_parameters,
					  self.tubing_parameters,
					  self.near_stabilizer_parameters,
					  self.string_stabilizer_parameters,
					  self.drilling_tools_parameters]

		for parameter in parameters:
			if parameter:
				if parameter == self.drill_collar_parameters:
					for serial_no in self.drill_collar_parameters:
						if serial_no.status == "Validated":
							accepted_sn.append(serial_no.serial_no)
					self.accepted_serial_no = '\n'.join(str(sn) for sn in accepted_sn)

				if parameter == self.heavy_weight_drill_pipe_parameters:
					for serial_no in self.heavy_weight_drill_pipe_parameters:
						if serial_no.status == "Validated":
							accepted_sn.append(serial_no.serial_no)
					self.accepted_serial_no = '\n'.join(str(sn) for sn in accepted_sn)


		ro = frappe.get_doc("Rental Order", self.rental_order)
		for item in ro.items:
			if item.item_code == self.item_code:
				item.serial_no_accepted = self.accepted_serial_no
				ro.save()
				frappe.db.commit()
		


@frappe.whitelist()
def create_wo(qty,bom,purpose,item_code,warehouse=None,item_category=None,project=None,project_wo=None,sales_o=None,rental_o=None):
	new_doc = frappe.new_doc('Work Order')
	if float(qty) == 0:
		frappe.throw(_("You don't have Item : {} in warehouse {}")
					.format(item_code,warehouse))
	if rental_o:
		qty_wo = frappe.db.sql("""select qty
								  from `tabWork Order` 
								  where rental_order = "%s" 
								  and production_item = "%s" 
								  and status != "Cancelled" """ %(rental_o,item_code),as_dict=1)
		qty_list = []
		for i in range(len(qty_wo)):   
			qty_list.append(qty_wo[i]['qty'])
		total_wo_qty = sum(qty_list)
		if float(total_wo_qty) + float(qty) > get_rental_order_item_qty(rental_o,item_code):
			frappe.throw(_("Cannot inspect more Item {} than Rental Order quantity {}"
			.format(item_code,get_rental_order_item_qty(rental_o,item_code))))

	item_bom = frappe.db.get_value("BOM",bom,"inspection_bom")
	if item_bom != 1 and purpose == "Inspection":
		frappe.throw(_("You're selecting a manufacturing BOM for inspection purpose"))
	elif item_bom == 1 and purpose == "Manufacturing":
		frappe.throw(_("You're selecting an inspection BOM for manufacturing purpose"))

	department = frappe.db.get_list('Department', pluck='name')
	if purpose == "Inspection":
		for d in department:
			if "Inspection" in d:	
				new_doc.department_ = d
	else:
		for d in department:
			if "Manufacturing" in d:	
				new_doc.department_ = d

	new_doc.division = frappe.db.get_value("Project",project,'Division')
	new_doc.skip_transfer = 1
	new_doc.date = frappe.utils.nowdate()
	new_doc.fg_warehouse = warehouse
	new_doc.production_item = item_code
	new_doc.item_category = item_category
	new_doc.qty = float(qty)
	new_doc.sales_order = sales_o
	new_doc.rental_order = rental_o
	new_doc.project = project
	new_doc.project_wo = project_wo
	new_doc.bom_no = bom
	new_doc.save()
	frappe.db.commit()
	return "dddddd"

def get_q_i_t_p(item_code,parameter):
	qit = frappe.db.get_value("Item",item_code,"quality_inspection_template")
	doc = frappe.get_doc("Quality Inspection Template",qit)
	min_value = 0
	max_value = 0 
	for row in doc.item_quality_inspection_parameter:
		if row.specification == parameter:
			min_value = row.min_value
			max_value = row.max_value
	return {'min_value':min_value,'max_value':max_value}


def get_rental_order_item_qty(rental_o,item_code):
    item_qty = frappe.db.sql("""select qty
                                from `tabRental Order Item` 
                                where item_code = "%s" and parent = "%s" """ %(item_code,rental_o), as_dict=1)
    return item_qty[0]['qty']




def get_list():
	department = frappe.db.get_list('Department', pluck='name')
	for d in department:
		if "Inspection" in d:
			depar = d
			print(d)