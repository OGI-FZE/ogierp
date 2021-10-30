
from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "fieldname": "rental_order",
        "internal_links": {
            "Rental Quotation": ["items", 'rental_quotation'],
            "Rental Estimation": ["items", 'rental_estimation'],
        },
        "transactions": [
            {
                'label': _('Transactions'),
                'items': ['Rental Quotation', "Rental Estimation", "Rental Issue Note", "Sales Invoice"]
            },
            {
                'label': _('References'),
                'items': ['Material Request', "Asset Formation", "Purchase Order", "Purchase Invoice"]
            },
        ]
    }
