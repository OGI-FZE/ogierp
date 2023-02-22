from frappe.model.document import Document, _
import frappe
from fractions import Fraction
import collections


class Inspection(Document):
	def validate(self):
		if frappe.db.get_value('Item',self.item_code,"has_serial_no") ==0:
			self.for_external_inspection = 1
		if self.pending_quantity == 0:
			frappe.throw(_("All serial No are inspected"))
		i = self.item_code
		warehouse_qty = frappe.db.get_value("Bin",{"item_code":self.item_code,"warehouse":self.warehouse},"actual_qty")
		if not warehouse_qty:
			warehouse_qty = 0

		parameters = [self.drill_collar_parameters,
					  self.heavy_weight_drill_pipe_parameters,
					  self.drill_pipe_parameters,
					  self.near_stabilizer_parameters,
					  self.string_stabilizer_parameters,
					  self.drilling_tools_parameters]
		for parameter in parameters:
			serial_no_list = []
			if parameter and parameter == self.drill_collar_parameters:
					if float(warehouse_qty) < len(parameter):
						frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
					for serial_no in self.drill_collar_parameters:
						if self.for_external_inspection:
							serial_no_list.append(serial_no.customer_serial_no)
						else:
							serial_no_list.append(serial_no.serial_no)
						duplicated = [sn for sn, count in collections.Counter(serial_no_list).items() if count > 1]
						if self.for_external_inspection:
							if serial_no.customer_serial_no in duplicated:
								frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.customer_serial_no)))
						else:
							if serial_no.serial_no in duplicated:
								frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.serial_no)))
						if self.for_external_inspection:
							check_duplicated_serial_no(serial_no.customer_serial_no,self.work_order)
						else:
							check_duplicated_serial_no(serial_no.serial_no,self.work_order)
						conditions = [not get_q_i_t_p(i,"length")['min_value'] <= to_frac(serial_no.length) <= get_q_i_t_p(i,"length")['max_value'] or
								not get_q_i_t_p(i,"OD")['min_value'] <= to_frac(serial_no.od) <= get_q_i_t_p(i,"OD")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= to_frac(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"SRG Dia")['min_value'] <= to_frac(serial_no.srg_dia) <= get_q_i_t_p(i,"SRG Dia")['max_value'] or
								not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= to_frac(serial_no.bevel_dia) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"SRG Width")['min_value'] <= to_frac(serial_no.srg_width) <= get_q_i_t_p(i,"SRG Width")['max_value'] or
								not get_q_i_t_p(i,"Neck Length")['min_value'] <= to_frac(serial_no.neck_length) <= get_q_i_t_p(i,"Neck Length")['max_value'] or
								not get_q_i_t_p(i,"Pin Tong Space")['min_value'] <= to_frac(serial_no.pin_tong_space) <= get_q_i_t_p(i,"Pin Tong Space")['max_value'] or
								not get_q_i_t_p(i,"Box OD")['min_value'] <= to_frac(serial_no.box_od) <= get_q_i_t_p(i,"Box OD")['max_value'] or
								not get_q_i_t_p(i,"Box Bevel Dia")['min_value'] <= to_frac(serial_no.box_bevel_dia) <= get_q_i_t_p(i,"Box Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"Counter Bore Depth")['min_value'] <= to_frac(serial_no.counter_bore_depth) <= get_q_i_t_p(i,"Counter Bore Depth")['max_value'] or
								not get_q_i_t_p(i,"Counter Bore Dia")['min_value'] <= to_frac(serial_no.counter_bore_dia) <= get_q_i_t_p(i,"Counter Bore Dia")['max_value'] or
								not get_q_i_t_p(i,"Boreback Length")['min_value'] <= to_frac(serial_no.bo_boreback_length) <= get_q_i_t_p(i,"Boreback Length")['max_value'] or
								not get_q_i_t_p(i,"Boreback Diameter")['min_value'] <= to_frac(serial_no.boreback_dia) <= get_q_i_t_p(i,"Boreback Diameter")['max_value'] or
								not get_q_i_t_p(i,"Recess Gr OD")['min_value'] <= to_frac(serial_no.recess_groove_od) <= get_q_i_t_p(i,"Recess Gr OD")['max_value'] or
								not get_q_i_t_p(i,"Elevator Recess Depth")['min_value'] <= to_frac(serial_no.recess_groove_elevator) <= get_q_i_t_p(i,"Elevator Recess Depth")['max_value'] or
								not get_q_i_t_p(i,"Slip Recess Depth")['min_value'] <= to_frac(serial_no.recess_groove_slip) <= get_q_i_t_p(i,"Slip Recess Depth")['max_value'] 

								]
						if conditions[0]:
							serial_no.status= "Failed"
						else: 
							serial_no.status= "Validated"

			elif parameter and parameter == self.heavy_weight_drill_pipe_parameters:
				if float(warehouse_qty) < len(parameter):
					frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
				for serial_no in self.heavy_weight_drill_pipe_parameters:
					if self.for_external_inspection:
						serial_no_list.append(serial_no.customer_serial_no)
					else:
						serial_no_list.append(serial_no.serial_no)
					duplicated = [sn for sn, count in collections.Counter(serial_no_list).items() if count > 1]
					if self.for_external_inspection:
						if serial_no.customer_serial_no in duplicated:
							frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.customer_serial_no)))
					else:
						if serial_no.serial_no in duplicated:
							frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.serial_no)))
					if self.for_external_inspection:
						check_duplicated_serial_no(serial_no.customer_serial_no,self.work_order)
					else:
						check_duplicated_serial_no(serial_no.serial_no,self.work_order)	
					conditions = [not get_q_i_t_p(i,"length")['min_value'] <= to_frac(serial_no.length) <= get_q_i_t_p(i,"length")['max_value'] or
							not get_q_i_t_p(i,"OD")['min_value'] <= to_frac(serial_no.od) <= get_q_i_t_p(i,"OD")['max_value'] or
							not get_q_i_t_p(i,"ID")['min_value'] <= to_frac(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
							not get_q_i_t_p(i,"Internal Coating")['min_value'] <= to_frac(serial_no.internal_coating) <= get_q_i_t_p(i,"Internal Coating")['max_value'] or
							not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= to_frac(serial_no.bevel_dia) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
							not get_q_i_t_p(i,"SRG Dia")['min_value'] <= to_frac(serial_no.srg_dia) <= get_q_i_t_p(i,"SRG Dia")['max_value'] or
							not get_q_i_t_p(i,"SRG Width")['min_value'] <= to_frac(serial_no.srg_width) <= get_q_i_t_p(i,"SRG Width")['max_value'] or
							not get_q_i_t_p(i,"Pin Nose Dia")['min_value'] <= to_frac(serial_no.pin_nose_dia) <= get_q_i_t_p(i,"Pin Nose Dia")['max_value'] or
							not get_q_i_t_p(i,"Pin Cyl. Dia")['min_value'] <= to_frac(serial_no.pin_cyl_dia) <= get_q_i_t_p(i,"Pin Cyl. Dia")['max_value'] or
							not get_q_i_t_p(i,"Pin Tong Space")['min_value'] <= to_frac(serial_no.pin_tong_space) <= get_q_i_t_p(i,"Pin Tong Space")['max_value'] or
							not get_q_i_t_p(i,"Pin Connection Lenght/Neck Length")['min_value'] <= to_frac(serial_no.pin_connection_length) <= get_q_i_t_p(i,"Pin Connection Lenght/Neck Length")['max_value'] or
							not get_q_i_t_p(i,"Box OD")['min_value'] <= to_frac(serial_no.box_od) <= get_q_i_t_p(i,"Box OD")['max_value'] or
							not get_q_i_t_p(i,"Box Bevel Dia")['min_value'] <= to_frac(serial_no.box_bevel_dia) <= get_q_i_t_p(i,"Box Bevel Dia")['max_value'] or
							not get_q_i_t_p(i,"Counter Bore Depth")['min_value'] <= to_frac(serial_no.counter_bore_depth) <= get_q_i_t_p(i,"Counter Bore Depth")['max_value'] or
							not get_q_i_t_p(i,"Counter Bore Dia")['min_value'] <= to_frac(serial_no.counter_bore_dia) <= get_q_i_t_p(i,"Counter Bore Dia")['max_value'] or
							not get_q_i_t_p(i,"Box Seal Width")['min_value'] <= to_frac(serial_no.seal_width) <= get_q_i_t_p(i,"Box Seal Width")['max_value'] or
							not get_q_i_t_p(i,"Box Connection Length")['min_value'] <= to_frac(serial_no.box_connection_length) <= get_q_i_t_p(i,"Box Connection Length")['max_value'] or
							not get_q_i_t_p(i,"Bore Back Dia")['min_value'] <= to_frac(serial_no.boreback_dia) <= get_q_i_t_p(i,"Bore Back Dia")['max_value'] or
							not get_q_i_t_p(i,"OD Height")['min_value'] <= to_frac(serial_no.od_height) <= get_q_i_t_p(i,"OD Height")['max_value'] or
							not get_q_i_t_p(i,"Box Tong Space")['min_value'] <= to_frac(serial_no.box_tong_space) <= get_q_i_t_p(i,"Box Tong Space")['max_value'] 
						
						]
					if conditions[0]:
						serial_no.status= "Failed"
					else: 
						serial_no.status= "Validated"
			elif parameter and parameter == self.drill_pipe_parameters:
					if float(warehouse_qty) < len(parameter):
						frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
					for serial_no in self.drill_pipe_parameters:
						if self.for_external_inspection:
							serial_no_list.append(serial_no.customer_serial_no)
						else:
							serial_no_list.append(serial_no.serial_no)
						duplicated = [sn for sn, count in collections.Counter(serial_no_list).items() if count > 1]
						if self.for_external_inspection:
							if serial_no.customer_serial_no in duplicated:
								frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.customer_serial_no)))
						else:
							if serial_no.serial_no in duplicated:
								frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.serial_no)))
						if self.for_external_inspection:
							check_duplicated_serial_no(serial_no.customer_serial_no,self.work_order)
						else:
							check_duplicated_serial_no(serial_no.serial_no,self.work_order)
						conditions = [not get_q_i_t_p(i,"length")['min_value'] <= to_frac(serial_no.length) <= get_q_i_t_p(i,"length")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= to_frac(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"Remaining Wall Thickness")['min_value'] <= to_frac(serial_no.remaining_wall_thickness) <= get_q_i_t_p(i,"Remaining Wall Thickness")['max_value'] or
								not get_q_i_t_p(i,"Internal Coating")['min_value'] <= to_frac(serial_no.internal_coating) <= get_q_i_t_p(i,"Internal Coating")['max_value'] or
								not get_q_i_t_p(i,"Pin Connection Length")['min_value'] <= to_frac(serial_no.pin_connection_length) <= get_q_i_t_p(i,"Pin Connection Length")['max_value'] or
								not get_q_i_t_p(i,"Pin Nose Dia")['min_value'] <= to_frac(serial_no.pin_nose_dia) <= get_q_i_t_p(i,"Pin Nose Dia")['max_value'] or
								not get_q_i_t_p(i,"Pin Cyl. Dia")['min_value'] <= to_frac(serial_no.pin_cyl_dia) <= get_q_i_t_p(i,"Pin Cyl. Dia")['max_value'] or
								not get_q_i_t_p(i,"Pin Neck LengtH")['min_value'] <= to_frac(serial_no.pin_neck_length) <= get_q_i_t_p(i,"Pin Neck LengtH")['max_value'] or
								not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= to_frac(serial_no.bevel_dia) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"Pin Tong Space")['min_value'] <= to_frac(serial_no.pin_tong_space) <= get_q_i_t_p(i,"Pin Tong Space")['max_value'] or
								not get_q_i_t_p(i,"Box OD")['min_value'] <= to_frac(serial_no.box_od) <= get_q_i_t_p(i,"Box OD")['max_value'] or
								not get_q_i_t_p(i,"Box Bevel Dia")['min_value'] <= to_frac(serial_no.box_bevel_dia) <= get_q_i_t_p(i,"Box Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"Box Connection Length")['min_value'] <= to_frac(serial_no.box_connection_length) <= get_q_i_t_p(i,"Box Connection Length")['max_value'] or
								not get_q_i_t_p(i,"Shoulder width/Counter Bore wall")['min_value'] <= to_frac(serial_no.shoulder_width_counter_bore_wall) <= get_q_i_t_p(i,"Shoulder width/Counter Bore wall")['max_value'] or
								not get_q_i_t_p(i,"Counter Bore Dia")['min_value'] <= to_frac(serial_no.counter_bore_dia) <= get_q_i_t_p(i,"Counter Bore Dia")['max_value'] or
								not get_q_i_t_p(i,"Counter Bore Depth")['min_value'] <= to_frac(serial_no.counter_bore_depth) <= get_q_i_t_p(i,"Counter Bore Depth")['max_value'] or
								not get_q_i_t_p(i,"Box Tong Space")['min_value'] <= to_frac(serial_no.box_tong_space) <= get_q_i_t_p(i,"Box Tong Space")['max_value'] 

						]
						if conditions[0]:
							serial_no.status= "Failed"
						else: 
							serial_no.status= "Validated"

			elif parameter and parameter == self.string_stabilizer_parameters:
					if float(warehouse_qty) < len(parameter):
						frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
					for serial_no in self.string_stabilizer_parameters:
						if self.for_external_inspection:
							serial_no_list.append(serial_no.customer_serial_no)
						else:
							serial_no_list.append(serial_no.serial_no)
						duplicated = [sn for sn, count in collections.Counter(serial_no_list).items() if count > 1]
						if self.for_external_inspection:
							if serial_no.customer_serial_no in duplicated:
								frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.customer_serial_no)))
						else:
							if serial_no.serial_no in duplicated:
								frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.serial_no)))
						if self.for_external_inspection:
							check_duplicated_serial_no(serial_no.customer_serial_no,self.work_order)
						else:
							check_duplicated_serial_no(serial_no.serial_no,self.work_order)
						conditions = [not get_q_i_t_p(i,"length")['min_value'] <= to_frac(serial_no.length) <= get_q_i_t_p(i,"length")['max_value'] or
								not get_q_i_t_p(i,"OD")['min_value'] <= to_frac(serial_no.od) <= get_q_i_t_p(i,"OD")['max_value'] or
								not get_q_i_t_p(i,"ID")['min_value'] <= to_frac(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
								not get_q_i_t_p(i,"Pin Tong Space")['min_value'] <= to_frac(serial_no.tong_space) <= get_q_i_t_p(i,"Pin Tong Space")['max_value'] or
								not get_q_i_t_p(i,"Pin Thread Length")['min_value'] <= to_frac(serial_no.pin_thread_length) <= get_q_i_t_p(i,"Pin Thread Length")['max_value'] or
								not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= to_frac(serial_no.bevel_dia) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"SRG Dia")['min_value'] <= to_frac(serial_no.srg_dia) <= get_q_i_t_p(i,"SRG Dia")['max_value'] or
								not get_q_i_t_p(i,"SRG Length")['min_value'] <= to_frac(serial_no.srg_length) <= get_q_i_t_p(i,"SRG Length")['max_value'] or
								not get_q_i_t_p(i,"Pin Neck LengtH")['min_value'] <= to_frac(serial_no.pin_neck_length) <= get_q_i_t_p(i,"Pin Neck LengtH")['max_value'] or
								not get_q_i_t_p(i,"Box OD")['min_value'] <= to_frac(serial_no.box_od) <= get_q_i_t_p(i,"Box OD")['max_value'] or
								not get_q_i_t_p(i,"Fishing Neck Length")['min_value'] <= to_frac(serial_no.fishing_neck_length) <= get_q_i_t_p(i,"Fishing Neck Length")['max_value'] or
								not get_q_i_t_p(i,"Qc Diameter")['min_value'] <= to_frac(serial_no.qc_diameter) <= get_q_i_t_p(i,"Qc Diameter")['max_value'] or
								not get_q_i_t_p(i,"Qc Depth")['min_value'] <= to_frac(serial_no.qc_depth) <= get_q_i_t_p(i,"Qc Depth")['max_value'] or
								not get_q_i_t_p(i,"Boreback Diameter")['min_value'] <= to_frac(serial_no.boreback_diameter) <= get_q_i_t_p(i,"Boreback Diameter")['max_value'] or
								not get_q_i_t_p(i,"Boreback Length")['min_value'] <= to_frac(serial_no.boreback_length) <= get_q_i_t_p(i,"Boreback Length")['max_value'] or
 								not get_q_i_t_p(i,"Box Bevel Dia")['min_value'] <= to_frac(serial_no.box_bevel_dia) <= get_q_i_t_p(i,"Box Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"Box Seal Width")['min_value'] <= to_frac(serial_no.box_seal_width) <= get_q_i_t_p(i,"Box Seal Width")['max_value'] 

								]
						try: 
							if conditions[0]:
								serial_no.status= "Failed"
							else: 
								serial_no.status= "Validated"
						except TypeError:
							frappe.throw_error(_("Fill fields properly to preceed the verification"))
			elif parameter and parameter == self.near_stabilizer_parameters:
					if float(warehouse_qty) < len(parameter):
						frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
					for serial_no in self.near_stabilizer_parameters:
						if self.for_external_inspection:
							serial_no_list.append(serial_no.customer_serial_no)
						else:
							serial_no_list.append(serial_no.serial_no)
						duplicated = [sn for sn, count in collections.Counter(serial_no_list).items() if count > 1]
						if self.for_external_inspection:
							if serial_no.customer_serial_no in duplicated:
								frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.customer_serial_no)))
						else:
							if serial_no.serial_no in duplicated:
								frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.serial_no)))
						if self.for_external_inspection:
							check_duplicated_serial_no(serial_no.customer_serial_no,self.work_order)
						else:
							check_duplicated_serial_no(serial_no.serial_no,self.work_order)
						
						conditions = [not get_q_i_t_p(i,"length")['min_value'] <= to_frac(serial_no.length) <= get_q_i_t_p(i,"length")['max_value'] or
								not get_q_i_t_p(i,"OD")['min_value'] <= to_frac(serial_no.od) <= get_q_i_t_p(i,"OD")['max_value'] or
								not get_q_i_t_p(i,"Fish neck Length")['min_value'] <= to_frac(serial_no.fishneck_length) <= get_q_i_t_p(i,"Fish neck Length")['max_value'] or
								not get_q_i_t_p(i,"Qc Diameter")['min_value'] <= to_frac(serial_no.qc_diameter) <= get_q_i_t_p(i,"Qc Diameter")['max_value'] or
								not get_q_i_t_p(i,"Qc Depth")['min_value'] <= to_frac(serial_no.qc_depth) <= get_q_i_t_p(i,"Qc Depth")['max_value'] or
								not get_q_i_t_p(i,"Boreback Diameter")['min_value'] <= to_frac(serial_no.boreback_diameter) <= get_q_i_t_p(i,"Boreback Diameter")['max_value'] or
								not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= to_frac(serial_no.bevel_diameter) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
								not get_q_i_t_p(i,"Box Seal Width")['min_value'] <= to_frac(serial_no.box_seal_width) <= get_q_i_t_p(i,"Box Seal Width")['max_value'] 
						]
						if conditions[0]:
							serial_no.status = "Failed"
						else: 
							serial_no.status = "Validated"
			elif parameter and parameter == self.drilling_tools_parameters:
						if float(warehouse_qty) < len(parameter):
							frappe.throw(_("You dont have all this quantity in Warehouse {}".format(self.warehouse)))
						for serial_no in self.drilling_tools_parameters:
							if self.for_external_inspection:
								serial_no_list.append(serial_no.customer_serial_no)
							else:
								serial_no_list.append(serial_no.serial_no)
							duplicated = [sn for sn, count in collections.Counter(serial_no_list).items() if count > 1]
							if self.for_external_inspection:
								if serial_no.customer_serial_no in duplicated:
									frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.customer_serial_no)))
							else:
								if serial_no.serial_no in duplicated:
									frappe.throw(_("{} is duplicated, please re-check Serial No filled".format(serial_no.serial_no)))
							if self.for_external_inspection:
								check_duplicated_serial_no(serial_no.customer_serial_no,self.work_order)
							else:
								check_duplicated_serial_no(serial_no.serial_no,self.work_order)	
							conditions = [not get_q_i_t_p(i,"length")['min_value'] <= to_frac(serial_no.length) <= get_q_i_t_p(i,"length")['max_value'] or
									not get_q_i_t_p(i,"OD")['min_value'] <= to_frac(serial_no.od) <= get_q_i_t_p(i,"OD")['max_value'] or
									not get_q_i_t_p(i,"ID")['min_value'] <= to_frac(serial_no.id) <= get_q_i_t_p(i,"ID")['max_value'] or
									not get_q_i_t_p(i,"Pin Connection Length")['min_value'] <= to_frac(serial_no.pin_connection_length_neck_length) <= get_q_i_t_p(i,"Pin Connection Length")['max_value'] or
									not get_q_i_t_p(i,"Pin Tong Space")['min_value'] <= to_frac(serial_no.pin_tong_space) <= get_q_i_t_p(i,"Pin Tong Space")['max_value'] or
									not get_q_i_t_p(i,"Bevel Dia")['min_value'] <= to_frac(serial_no.bevel_dia) <= get_q_i_t_p(i,"Bevel Dia")['max_value'] or
									not get_q_i_t_p(i,"SRG Dia")['min_value'] <= to_frac(serial_no.srg_dia) <= get_q_i_t_p(i,"SRG Dia")['max_value'] or
									not get_q_i_t_p(i,"SRG Width")['min_value'] <= to_frac(serial_no.srg_width) <= get_q_i_t_p(i,"SRG Width")['max_value'] or
									not get_q_i_t_p(i,"Pin Nose Dia")['min_value'] <= to_frac(serial_no.pin_nose_dia) <= get_q_i_t_p(i,"Pin Nose Dia")['max_value'] or
									not get_q_i_t_p(i,"Box OD")['min_value'] <= to_frac(serial_no.box_od) <= get_q_i_t_p(i,"Box OD")['max_value'] or
									not get_q_i_t_p(i,"Box Tong Space")['min_value'] <= to_frac(serial_no.box_tong_space) <= get_q_i_t_p(i,"Box Tong Space")['max_value'] or
									not get_q_i_t_p(i,"CB Depth")['min_value'] <= to_frac(serial_no.cb_depth) <= get_q_i_t_p(i,"CB Depth")['max_value'] or
									not get_q_i_t_p(i,"CB Dia")['min_value'] <= to_frac(serial_no.cb_dia) <= get_q_i_t_p(i,"CB Dia")['max_value'] or
									not get_q_i_t_p(i,"Box Bevel Dia")['min_value'] <= to_frac(serial_no.box_bevel_dia) <= get_q_i_t_p(i,"Box Bevel Dia")['max_value'] or
									not get_q_i_t_p(i,"BB/ FB Dia")['min_value'] <= to_frac(serial_no.bb_fb_dia) <= get_q_i_t_p(i,"BB/ FB Dia")['max_value'] or
									not get_q_i_t_p(i,"BB/FB Length/ Connection Length")['min_value'] <= to_frac(serial_no.bb_fb_le_cnc) <= get_q_i_t_p(i,"BB/FB Length/ Connection Length")['max_value'] or
									not get_q_i_t_p(i,"Shoulder Width/CB wall Thick.")['min_value'] <= to_frac(serial_no.shoulder_width_cb_wall_thick) <= get_q_i_t_p(i,"Shoulder Width/CB wall Thick.")['max_value'] 
							]
							if conditions[0]:
								serial_no.status = "Failed"
							else: 
								serial_no.status = "Validated"


	def before_submit(self):
		accepted_sn = []
		parameters = [self.drill_collar_parameters,
					  self.heavy_weight_drill_pipe_parameters,
					  self.drill_pipe_parameters,
					  self.near_stabilizer_parameters,
					  self.string_stabilizer_parameters,
					  self.drilling_tools_parameters]

		for parameter in parameters:
			if parameter:
					for serial_no in parameter:
						if serial_no.status == "Validated":
							if self.for_external_inspection:
								accepted_sn.append(serial_no.customer_serial_no)
							else:
								accepted_sn.append(serial_no.serial_no)
					self.accepted_serial_no = '\n'.join(str(sn) for sn in accepted_sn)
					self.total_inspected = len(accepted_sn)
					if self.total_inspected > self.pending_quantity:
						frappe.throw(_("You overpassed the quantity required"))
		fill_order_serial_no(self.for_external_inspection,self.item_code,self.accepted_serial_no,self.work_order,self.rental_order,self.sales_order)

	def on_submit(self):
		if self.work_order:
			self.total_inspected_for_order = get_total_inspected(self.work_order)

	def on_cancel(self):
		delete_cancelled_inspection_serial_no(self.for_external_inspection,self.item_code,self.work_order,self.accepted_serial_no,self.rental_order,self.sales_order)



		
@frappe.whitelist()
def create_wo(qty,bom,purpose,item_code,warehouse=None,item_category=None,for_cu_ins=None,project=None,project_wo=None,sales_o=None,rental_o=None):
	if for_cu_ins==1:
		stock_entry = frappe.db.get_value("Stock Entry", {"sales_order": sales_o},'name')
		stock_entry_qty = get_stock_entry_qty(stock_entry,item_code)
		qty_wo = frappe.db.sql("""select qty
								  from `tabWork Order` 
								  where sales_order = "%s" 
								  and production_item = "%s" 
								  and status != "Cancelled" """ %(sales_o,item_code),as_dict=1) 
		qty_list = []
		for i in range(len(qty_wo)):   
			qty_list.append(qty_wo[i]['qty'])
		total_wo_qty = sum(qty_list)
		if float(total_wo_qty) + float(qty) > float(stock_entry_qty):
			frappe.throw(_("Cannot inspect more Item {} than Stock Entry quantity {}"
			.format(item_code,get_stock_entry_qty(stock_entry,item_code))))

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
	new_doc.for_external_inspection = for_cu_ins
	new_doc.save()
	frappe.db.commit()
	return "dddddd"

def get_q_i_t_p(item_code,parameter):
	qit = frappe.db.get_value("Item",item_code,"quality_inspection_template")
	if not qit:
		frappe.throw(_("Please set the Quality Inspection Template for this item"))
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

def get_stock_entry_qty(stock_entry,item_code):
    item_qty = frappe.db.sql("""select qty
                                from `tabStock Entry Detail` 
                                where item_code = "%s" and parent = "%s" """ %(item_code,stock_entry), as_dict=1)
    return item_qty[0]['qty']

def get_list():
	department = frappe.db.get_list('Department', pluck='name')
	for d in department:
		if "Inspection" in d:
			depar = d
			print(d)
 
@frappe.whitelist()
def get_total_inspected(work_order= None):
	qty = 0
	inspected = frappe.db.sql('''select sum(total_inspected) from `tabInspection` where work_order = '%s' and
								 docstatus != 2 '''% format(work_order) )

	return inspected[0][0]

def to_frac(a):
	value = a
	if "-" in a:
		b = a.split("-")
		value = float(b[0])+Fraction(b[1]) 
	else:
		value = float(a)
	return value

@frappe.whitelist()
def change_wo_qty(work_order=None,total_inspected_for_order=None,total_inspected=None):
	wo = frappe.get_doc("Work Order",work_order )
	wo.total_inspected = get_total_inspected(work_order)
	wo.pending_to_inspect = wo.qty - float(total_inspected_for_order)
	wo.save()
	frappe.db.commit()



@frappe.whitelist()
def fill_order_serial_no(for_external_inspection,item_code,accepted_serial_no,work_order,rental_order,sales_order):
	if rental_order or sales_order:
		if rental_order:
			order = frappe.get_doc("Rental Order", rental_order)
		elif sales_order:
			order = frappe.get_doc("Sales Order", sales_order)

		for item in order.items:
			if for_external_inspection:
				if order.customer_accepted_serial_no:
					order.customer_accepted_serial_no = '\n'.join([order.customer_accepted_serial_no,accepted_serial_no])
					order.save()
				else:
					order.set('customer_accepted_serial_no',accepted_serial_no)
					order.save()
					frappe.db.commit()
			if item.item_code == item_code:
				if len(frappe.db.get_list("Inspection",filters={"work_order":work_order,"docstatus":['!=',2]})) == 1:
					item.set("serial_no_accepted",accepted_serial_no)
					order.save()
					frappe.db.commit()

				else:
					item.serial_no_accepted = '\n'.join([item.serial_no_accepted,accepted_serial_no])
					order.save()
					frappe.db.commit() 



def check_duplicated_serial_no(serial_no=None,work_order=None):
	sn = frappe.db.sql("""select accepted_serial_no
						  from `tabInspection` 
						  where work_order = '%s' and docstatus = 1"""% format(work_order), as_dict=1)
	sn_list = []
	print(sn)
	for r in range(len(sn)):
		temporary = sn[r]['accepted_serial_no'].split("\n")
		for t in temporary:
			sn_list.append(t)
		if serial_no in sn_list:
			frappe.throw(_("Serial No {} is already inspected and validated, please delete it from the table".format(serial_no)))


def delete_cancelled_inspection_serial_no(for_external_inspection,item_code,work_order,accepted_serial_no,rental_order,sales_order):
	if work_order:
		wo = frappe.get_doc("Work Order",work_order)
		inspection_sn_no = accepted_serial_no.split('\n')
		wo.pending_to_inspect += len(inspection_sn_no)
		wo.total_inspected -= len(inspection_sn_no)
		wo.save()
		frappe.db.commit()
	if rental_order or sales_order:
		if rental_order:
			order = frappe.get_doc("Rental Order", rental_order)
		elif sales_order:
			order = frappe.get_doc("Sales Order", sales_order)
		if for_external_inspection==1:
			order_sn_no = order.customer_accepted_serial_no.split('\n')
			for i in inspection_sn_no:
				order_sn_no.remove(i)
				order.set("customer_accepted_serial_no","\n".join(order_sn_no))
				order.save()
				frappe.db.commit()
		for item in order.items:
			if item.item_code == item_code:
				order_sn_no = item.serial_no_accepted.split('\n')
				for i in inspection_sn_no:
					order_sn_no.remove(i)
					item.set("serial_no_accepted","\n".join(order_sn_no))
					order.save()
					frappe.db.commit()



