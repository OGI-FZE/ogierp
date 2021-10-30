
from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "fieldname": "rental_receipt_note",
        "internal_links": {
            "Rental Order": ["items", 'rental_order'],
            "Rental Issue Note": ["items", 'rental_issue_note']
        },
        "transactions": [
            {
                'label': _('References'),
                'items': ['Rental Order', "Rental Issue Note"]
            },
        ]
    }
