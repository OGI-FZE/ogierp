
from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "fieldname": "rental_estimation",
        "internal_links": {
            "Opportunity": ["items", 'opportunity']
        },
        "transactions": [
            {
                'label': _('Fulfillment'),
                'items': ['Rental Quotation', 'Opportunity']
            },
        ]
    }
