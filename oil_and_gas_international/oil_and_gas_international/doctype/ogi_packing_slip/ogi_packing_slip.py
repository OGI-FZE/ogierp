from frappe.model.document import Document

class OGIPackingSlip(Document):
	def validate(self):

		from erpnext.utilities.transaction_base import validate_uom_is_integer
		validate_uom_is_integer(self, "stock_uom", "qty")
		validate_uom_is_integer(self, "weight_uom", "net_weight")
