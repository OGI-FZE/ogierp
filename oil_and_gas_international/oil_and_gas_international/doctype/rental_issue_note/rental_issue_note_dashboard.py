
from __future__ import unicode_literals
from frappe import _


def get_data():
    return {
        "fieldname": "rental_issue_note",
        "internal_links": {
            "Rental Order": ["items", 'rental_order']
        },
        "transactions": [
            {
                'label': _('References'),
                'items': ['Rental Order']
            },
        ]
    }
