
from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "fieldname": "rental_quotation",
        "internal_links": {
            "Rental Estimation": ["items", 'rental_estimate']
        },
        "transactions": [
            {
                'label': _('References'),
                'items': ['Rental Order', 'Rental Estimation']
            },
        ]
    }
